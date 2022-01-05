"""Auth revoke command."""

import logging

from ostorlab.apis import runner as apis_runner
from ostorlab.apis import revoke_api_key
from ostorlab import configuration_manager
from ostorlab.cli.auth import auth
from ostorlab.cli import console

logger = logging.getLogger(__name__)


@auth.auth.command()
def revoke():
    """Use this to revoke your API key."""

    config_manager = configuration_manager.ConfigurationManager()

    try:
        api_key_id = config_manager.get_api_key_id()
        runner = apis_runner.APIRunner()

        with console.console.status(f'[{console.CONSOLE_LOADING_TEXT_STYLES}]Revoking API key'):
            response = runner.execute(revoke_api_key.RevokeAPIKeyAPIRequest(api_key_id))
            if response.get('errors') is not None:
                console.console.print(f'[{console.CONSOLE_ERROR_TEXT_STYLES}]Could not revoke your API key.')

            runner.unauthenticate()
            config_manager.delete_api_data()
            console.console.print(
                f'[{console.CONSOLE_LOADED_TEXT_STYLES}]API key revoked')
    except apis_runner.AuthenticationError:
        runner.unauthenticate()
        console.console.print(
            f'[{console.CONSOLE_LOADING_TEXT_STYLES}]Your API key has already been revoked.')
