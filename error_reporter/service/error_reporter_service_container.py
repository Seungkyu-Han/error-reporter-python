from typing import Union

from error_reporter.core.core_client import CoreClient
from error_reporter.core.helper.error_message_format_helper import ErrorMessageFormatHelper
from error_reporter.error_reporter_options import SlackOptions


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

    raise Exception('invalid type')