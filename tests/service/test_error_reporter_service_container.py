import pytest

from error_reporter.error_reporter_options import (
    SlackOptions,
    DiscordOptions,
    GoogleChatOptions,
    GithubOptions,
)
from error_reporter.core.slack_client import SlackClient
from error_reporter.core.discord_client import DiscordClient
from error_reporter.core.google_chat_client import GoogleChatClient
from error_reporter.core.github_client import GithubClient
from error_reporter.service.error_reporter_service_container import get_client


def test_get_slack_client_correctly():
    options = SlackOptions(webhook_url="url", server_name="server")

    client = get_client(options)

    assert isinstance(client, SlackClient)
    assert client._webhook_url == "url"
    assert client._error_message_format_helper._server_name == "server"


def test_get_discord_client_correctly():
    options = DiscordOptions(webhook_url="url", server_name="server")

    client = get_client(options)

    assert isinstance(client, DiscordClient)
    assert client._webhook_url == "url"
    assert client._error_message_format_helper._server_name == "server"


def test_get_google_chat_client_correctly():
    options = GoogleChatOptions(webhook_url="url", server_name="server")

    client = get_client(options)

    assert isinstance(client, GoogleChatClient)
    assert client._webhook_url == "url"
    assert client._error_message_format_helper._server_name == "server"


def test_get_github_client_correctly():
    options = GithubOptions(
        github_token="token",
        owner="owner",
        repository="repo",
        server_name="server",
    )

    client = get_client(options)

    assert isinstance(client, GithubClient)
    assert client._github_token == "token"
    assert client._owner == "owner"
    assert client._repository == "repo"
    assert client._error_message_format_helper._server_name == "server"


def test_get_client_invalid_type():
    class Invalid:
        server_name = "server"

    with pytest.raises(Exception):
        get_client(options=Invalid)