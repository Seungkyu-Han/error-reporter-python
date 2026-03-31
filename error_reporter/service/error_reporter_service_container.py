from error_reporter.core.core_client import CoreClient
from error_reporter.core.helper.error_message_format_helper import ErrorMessageFormatHelper
from error_reporter.types.error_reporter_options import ErrorReporterOptions


def get_client(
        error_reporter_options: ErrorReporterOptions
) -> CoreClient:

    error_message_format_helper = ErrorMessageFormatHelper(
        server_name=error_reporter_options.server_name,
    )

    if error_reporter_options.type == 'slack':

        from error_reporter.core.slack_client import SlackClient

        return SlackClient(
            webhook_url=error_reporter_options.webhook_url,
            error_message_format_helper=error_message_format_helper,
        )

    raise Exception('invalid type')