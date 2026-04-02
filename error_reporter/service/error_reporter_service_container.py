from typing import Union

from error_reporter.core.core_client import CoreClient
from error_reporter.core.error_message_format_helper import ErrorMessageFormatHelper
from error_reporter.error_reporter_options import GoogleChatOptions, GithubOptions, SlackOptions, DiscordOptions


def get_client(
        options: Union[SlackOptions, DiscordOptions, GoogleChatOptions, GithubOptions]
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

    elif isinstance(options, GoogleChatOptions):

        from error_reporter.core.google_chat_client import GoogleChatClient

        return GoogleChatClient(
            webhook_url=options.webhook_url,
            error_message_format_helper=error_message_format_helper,
        )

    elif isinstance(options, GithubOptions):

        from error_reporter.core.github_client import GithubClient

        return GithubClient(
            github_token=options.github_token,
            owner=options.owner,
            repository=options.repository,
            error_message_format_helper=error_message_format_helper,
        )

    raise Exception('invalid type')
