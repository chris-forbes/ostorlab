# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ostorlab/agent/message/proto/v3/fingerprint/file/android/metadata/metadata.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nPostorlab/agent/message/proto/v3/fingerprint/file/android/metadata/metadata.proto\x12\x41ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata\">\n\x0cIntentFilter\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\t\"O\n\nPermission\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x19\n\x11protection_levels\x18\x02 \x03(\t\x12\x18\n\x10permission_group\x18\x03 \x01(\t\"\x84\x02\n\x08\x41\x63tivity\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\npermission\x18\x02 \x01(\t\x12\x0f\n\x07process\x18\x03 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x04 \x01(\x08\x12\x10\n\x08\x65xported\x18\x05 \x01(\x08\x12\x19\n\x11\x64irect_boot_aware\x18\x06 \x01(\x08\x12\x1e\n\x16\x61llow_task_reparenting\x18\x07 \x01(\x08\x12g\n\x0eintent_filters\x18\x08 \x03(\x0b\x32O.ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata.IntentFilter\"\xfe\x01\n\x07Service\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\npermission\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0f\n\x07process\x18\x04 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x05 \x01(\x08\x12\x10\n\x08\x65xported\x18\x06 \x01(\x08\x12\x1f\n\x17\x66oreground_service_type\x18\x07 \x01(\t\x12g\n\x0eintent_filters\x18\x08 \x03(\x0b\x32O.ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata.IntentFilter\"\xf0\x01\n\x08Provider\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\npermission\x18\x02 \x01(\t\x12\x0f\n\x07process\x18\x03 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x04 \x01(\x08\x12\x10\n\x08\x65xported\x18\x05 \x01(\x08\x12\x10\n\x08syncable\x18\x06 \x01(\x08\x12\x13\n\x0b\x61uthorities\x18\x07 \x03(\t\x12g\n\x0eintent_filters\x18\x08 \x03(\x0b\x32O.ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata.IntentFilter\"\xe4\x01\n\x08Receiver\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\npermission\x18\x02 \x01(\t\x12\x0f\n\x07process\x18\x03 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x04 \x01(\x08\x12\x10\n\x08\x65xported\x18\x05 \x01(\x08\x12\x19\n\x11\x64irect_boot_aware\x18\x06 \x01(\x08\x12g\n\x0eintent_filters\x18\x07 \x03(\x0b\x32O.ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata.IntentFilter\"\x82\x04\n\x07Message\x12\x14\n\x0cpackage_name\x18\x01 \x01(\t\x12\x62\n\x0bpermissions\x18\x02 \x03(\x0b\x32M.ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata.Permission\x12_\n\nactivities\x18\x03 \x03(\x0b\x32K.ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata.Activity\x12\\\n\x08services\x18\x04 \x03(\x0b\x32J.ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata.Service\x12^\n\tproviders\x18\x05 \x03(\x0b\x32K.ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata.Provider\x12^\n\treceivers\x18\x06 \x03(\x0b\x32K.ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata.Receiver')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ostorlab.agent.message.proto.v3.fingerprint.file.android.metadata.metadata_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _INTENTFILTER._serialized_start=151
  _INTENTFILTER._serialized_end=213
  _PERMISSION._serialized_start=215
  _PERMISSION._serialized_end=294
  _ACTIVITY._serialized_start=297
  _ACTIVITY._serialized_end=557
  _SERVICE._serialized_start=560
  _SERVICE._serialized_end=814
  _PROVIDER._serialized_start=817
  _PROVIDER._serialized_end=1057
  _RECEIVER._serialized_start=1060
  _RECEIVER._serialized_end=1288
  _MESSAGE._serialized_start=1291
  _MESSAGE._serialized_end=1805
# @@protoc_insertion_point(module_scope)
