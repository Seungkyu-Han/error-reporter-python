import pytest

from unittest.mock import MagicMock, patch, AsyncMock

from error_reporter.core.discord_client import DiscordClient
from error_reporter.types.message_builder_option import MessageBuilderOption


@pytest.fixture
def _mock_message() -> str:
    return "mock_message"


@pytest.fixture
def _mock_webhook_url() -> str:
    return "mock_webhook_url"


@pytest.fixture
def message_builder_option():
    return MessageBuilderOption()


@pytest.fixture
def _error_message_format_helper(_mock_message: str) -> MagicMock:
    helper = MagicMock()
    helper.error_message.return_value = _mock_message
    return helper


@pytest.fixture
def discord_client(_mock_webhook_url: str, _error_message_format_helper: MagicMock) -> DiscordClient:
    return DiscordClient(
        webhook_url=_mock_webhook_url,
        error_message_format_helper=_error_message_format_helper,
    )


def test_discord_client_init_correctly(
        discord_client: DiscordClient
):
    assert discord_client is not None
    assert discord_client._error_message_format_helper is not None


@pytest.mark.asyncio
@patch("error_reporter.core.discord_client.logger")
@patch("error_reporter.core.discord_client.aiohttp.ClientSession")
async def test_discord_client_report_correctly(
        mock_session_class: MagicMock,
        mock_logger: MagicMock,
        message_builder_option: str,
        discord_client: MagicMock,
):
    # given
    mock_response = AsyncMock()
    mock_response.status = 200

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    # when
    await discord_client.report(message_builder_option=message_builder_option)

    # then
    mock_session.post.assert_called_once()

    mock_logger.error.assert_not_called()
    mock_logger.info.assert_called_once()


@pytest.mark.asyncio
@patch("error_reporter.core.discord_client.logger")
@patch("error_reporter.core.discord_client.aiohttp.ClientSession")
async def test_discord_client_report_return_400_error(
        mock_session_class: MagicMock,
        mock_logger: MagicMock,
        message_builder_option: str,
        discord_client: MagicMock,
):
    # given
    mock_response = AsyncMock()
    mock_response.status = 400

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    # when
    await discord_client.report(message_builder_option=message_builder_option)

    # then
    mock_session.post.assert_called_once()

    mock_logger.info.assert_not_called()
    mock_logger.error.assert_called_once()


@pytest.mark.asyncio
@patch("error_reporter.core.discord_client.logger")
@patch("error_reporter.core.discord_client.aiohttp.ClientSession")
async def test_discord_client_report_raised_exception(
        mock_session_class: MagicMock,
        mock_logger: MagicMock,
        message_builder_option: str,
        discord_client: MagicMock,
):
    # given
    mock_response = AsyncMock()
    mock_response.status = 400

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.side_effect = Exception("network error")

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    # when
    await discord_client.report(message_builder_option=message_builder_option)

    # then
    mock_session.post.assert_called_once()

    mock_logger.info.assert_not_called()
    mock_logger.error.assert_called_once()
