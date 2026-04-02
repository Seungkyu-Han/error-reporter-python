from unittest.mock import MagicMock

from error_reporter.core.google_chat_client import GoogleChatClient


def test_google_chat_client_init_correctly(

):
    google_chat_client = GoogleChatClient(
        webhook_url="test",
        error_message_format_helper=MagicMock()
    )
    assert google_chat_client is not None