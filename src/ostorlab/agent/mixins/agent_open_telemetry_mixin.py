"""OpenTelemetry Mixin.

The mixin overrides the behaviour of the main methods of the agent, mainly emit and process to send traces,
metadata, metrics and exceptions.
"""
import io
import os
import logging
import uuid
from typing import Any, Dict, Optional
from urllib import parse
import json

from opentelemetry import trace
from opentelemetry.exporter.jaeger import thrift as jaeger
from opentelemetry.exporter import cloud_trace
from opentelemetry.sdk import trace as trace_provider
from opentelemetry.sdk.trace import export as sdk_export
from opentelemetry.sdk import resources

from ostorlab.runtimes import definitions as runtime_definitions
from ostorlab.agent import definitions as agent_definitions
from ostorlab.utils import dictionary_minifier
from ostorlab.agent import message as agent_message

logger = logging.getLogger(__name__)


class TraceExporter:
    """Class responsible for preparing the respective OpenTelemetry Span Exporter for an input tracing url."""

    def __init__(self, tracing_collector_url: str):
        self._tracing_collector_url = tracing_collector_url
        # specialized fields for the different collectors.
        self._file: Optional[io.IOBase] = None


    def close(self):
        if self._file is not None:
            self._file.close()

    def get_trace_exporter(self) -> sdk_export.SpanExporter:
        """
        Returns a span exporter instance depending on the OpenTelemtry collector url argument.
        The urls are customized to respect the following format:
            name_of_the_tracing_tool:hostname:port
            eg: jaeger:jaeger-host:8631
            for gcp the format is:
            name_of_the_tracing_tool:project_id:service_account_json_path
            eg: gcp:project_1:/tmp/key.json
        """
        parsed_url = parse.urlparse(self._tracing_collector_url)
        scheme = parsed_url.scheme
        if scheme == 'jaeger':
            return self._get_jaeger_exporter(parsed_url)
        elif scheme == 'file':
            return self._get_file_exporter(parsed_url)
        elif scheme == 'gcp':
            return self._get_gcp_exporter(parsed_url)
        else:
            raise NotImplementedError(f'Invalid tracer type {scheme}')

    def _get_file_exporter(self, parsed_url):
        file_path = parsed_url.path
        self._file = open(file_path, 'w', encoding='utf-8')  # pylint: disable=R1732
        file_exporter = sdk_export.ConsoleSpanExporter(out=self._file)
        logger.info('Configuring file exporter..')
        return file_exporter

    def _get_jaeger_exporter(self, parsed_url):
        netloc = parsed_url.netloc
        hostname, port = netloc.split(':')[0], int(netloc.split(':')[1])
        jaeger_exporter = jaeger.JaegerExporter(
            agent_host_name=hostname,
            agent_port=port,
            udp_split_oversized_batches=True,
        )
        logger.info('Configuring jaeger exporter..')
        return jaeger_exporter

    def _get_gcp_exporter(self, parsed_url: str) -> cloud_trace.CloudTraceSpanExporter:
        """
        Returns a CloudTraceSpan exporter instance.
        The urls should respect the following format:
            project_id:service_account_json_path
            eg: project_1:/tmp/key.json
        """
        parsed_path = parsed_url.path.split(':')
        project_id = parsed_path[0]
        service_account_key = parsed_path[1]
        # the env variable GOOGLE_APPLICATION_CREDENTIALS points to a file defining the service account credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_key
        return cloud_trace.CloudTraceSpanExporter(project_id=project_id)


class OpenTelemetryMixin:
    """OpenTelemetryMixin to send telemetry data of the agent behaviour. The mixin enables tracking information
    like when was a message processed or emitted, using which selector,
    how much time it took to serialize or deserialize a message, and report exceptions when they occur..etc.
    """

    _tracer: Optional[trace.Tracer] = None

    def __init__(self, agent_definition: agent_definitions.AgentDefinition,
                 agent_settings: runtime_definitions.AgentSettings) -> None:
        """Initializes the mixin from the agent settings.

        Args:
            agent_settings: Agent runtime settings.
        """
        super().__init__(agent_definition=agent_definition, agent_settings=agent_settings)
        self._agent_settings = agent_settings
        if self._agent_settings.tracing_collector_url is not None and self._agent_settings.tracing_collector_url != '':
            self._tracing_collector_url = self._agent_settings.tracing_collector_url
        else:
            self._tracing_collector_url = None

        if self._tracing_collector_url is not None:
            self._exporter = TraceExporter(self._tracing_collector_url)
            provider = trace_provider.TracerProvider(
                resource=resources.Resource.create({resources.SERVICE_NAME: agent_settings.key})
            )
            trace.set_tracer_provider(provider)
            self._span_processor = sdk_export.SimpleSpanProcessor(self._exporter.get_trace_exporter())
            trace.get_tracer_provider().add_span_processor(self._span_processor)
            self._tracer = trace.get_tracer(__name__)

    @property
    def tracer(self) -> trace.Tracer:
        """Tracer object to report traces to the configured opentelemetry collector.
        To use:

        ```python
        ...
        with self.tracer.start_as_current_span('<action>') as process_msg_span:
                process_msg_span.set_attribute('<attr1>', <value1>)
                ...
        ```
        """
        return self._tracer

    def force_flush_file_exporter(self) -> None:
        """Ensures persistence of the span details in the file for the case of the file Span exporters."""
        self._span_processor.force_flush()

    def _stringify_bytes_values(self, value: bytes):
        """Method that will be used as a handler to json dump the message dictionary values."""
        if isinstance(value, bytes):
            return value.decode()
        else:
            return value

    def process_message(self, selector: str, message: bytes) -> None:
        """Overridden agent process message method to add OpenTelemetry traces.
        Processes raw message received from BS.

        Args:
            selector: destination selector with full path, including UUID set by default.
            message: raw bytes message.

        Returns:
            None
        """
        if self._tracing_collector_url is not None:
            logger.debug('recording process message trace.')

            selector_split = selector.split('.')
            message_id = selector_split[-1]

            message_id_split = message_id.split('-')
            if len(message_id_split) > 5:
                # message is passing the message id, trace id and span id.
                trace_uuid = int(message_id_split[5])
                span_uuid = int(message_id_split[6])
                parent_span_context = trace.SpanContext(
                    trace_id=trace_uuid,
                    span_id=span_uuid,
                    is_remote=True,
                    trace_flags=trace.TraceFlags(0x01)
                )
                context = trace.set_span_in_context(trace.NonRecordingSpan(parent_span_context))
            else:
                context = {}

            raw_selector = '.'.join(selector_split[: -1])
            data = agent_message.Message.from_raw(raw_selector, message).data
            minified_msg_data = dictionary_minifier.minify_dict(data, dictionary_minifier.truncate_str)
            stringified_msg_data = json.dumps(minified_msg_data, default=self._stringify_bytes_values)

            with self.tracer.start_as_current_span('process_message', context=context) as process_msg_span:
                process_msg_span.set_attribute('agent.name', self.name)
                process_msg_span.set_attribute('message.selector', raw_selector)
                process_msg_span.set_attribute('message.data', stringified_msg_data)

                super().process_message(selector, message)
        else:
            super().process_message(selector, message)

    def emit(self, selector: str, data: Dict[str, Any], message_id: Optional[str] = None) -> None:
        """Overriden emit method of the agent to add OpenTelemetry traces.
        Sends a message to all listening agents on the specified selector.

        Args:
            selector: target selector.
            data: message data to be serialized.
            message_id: An id that will be added to the tail of the message.
        Raises:
            NonListedMessageSelectorError: when selector is not part of listed out selectors.

        Returns:
            None
        """
        if self._tracing_collector_url is not None:
            with self.tracer.start_as_current_span('emit_message') as emit_span:
                logger.debug('recording emit message trace..')

                trace_id = emit_span.get_span_context().trace_id
                span_id = emit_span.get_span_context().span_id

                emit_span.set_attribute('agent.name', self.name)
                emit_span.set_attribute('message.selector', selector)
                minified_msg_data = dictionary_minifier.minify_dict(data, dictionary_minifier.truncate_str)
                emit_span.set_attribute('message.data', json.dumps(minified_msg_data))

                super().emit(selector, data, f'{message_id or uuid.uuid4()}-{trace_id}-{span_id}')
        else:
            super().emit(selector, data)
