from typing import Union

from error_reporter import DiscordOptions, SlackOptions
from error_reporter.core.core_client import CoreClient
from error_reporter.core.helper.error_message_format_helper import ErrorMessageFormatHelper


def get_client(
        options: Union[SlackOptions]
) -> CoreClient:

    error_message_format_helper = ErrorMessageFormatHelper(
        server_name=options.server_name,
    )

    if isinstance(options, SlackOptions):

        from error_reporter.core.slack_client import SlackClient

        return SlackClient(
            webhook_url=options.webhook_url,
            error_message_format_helper=error_message_format_helper,
        )

    elif isinstance(options, DiscordOptions):

        from error_reporter.core.discord_client import DiscordClient

        return DiscordClient(
            webhook_url=options.webhook_url,
            error_message_format_helper=error_message_format_helper,
        )

    raise Exception('invalid type')