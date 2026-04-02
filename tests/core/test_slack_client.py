import pytest

from unittest.mock import Mock, AsyncMock, patch, MagicMock

from error_reporter.core.slack_client import SlackClient
from error_reporter.types.message_builder_option import MessageBuilderOption


@pytest.fixture
def mocked_message():
    return "mocked_message"


@pytest.fixture
def mocked_webhook_url():
    return "mocked_webhook_url"


@pytest.fixture
def message_builder_option():
    return MessageBuilderOption()


@pytest.fixture
def error_message_format_helper(mocked_message):
    helper = Mock()
    helper.error_message.return_value = mocked_message
    return helper


@pytest.fixture
def slack_client(mocked_webhook_url, error_message_format_helper):
    return SlackClient(
        webhook_url=mocked_webhook_url,
        error_message_format_helper=error_message_format_helper,
    )

def test_slack_client_correctly(
        slack_client: SlackClient
):
    assert slack_client is not None


@pytest.mark.asyncio
@patch("error_reporter.core.slack_client.logger")
@patch("error_reporter.core.slack_client.aiohttp.ClientSession")
async def test_slack_client_report_correctly(
    mock_session_class: MagicMock,
    mock_logger: MagicMock,
    slack_client: SlackClient,
    error_message_format_helper: MagicMock,
    message_builder_option: MessageBuilderOption,
    mocked_webhook_url: str,
    mocked_message: str,
) -> None:
    # given
    mock_response = AsyncMock()
    mock_response.status = 200

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    slack_client = SlackClient(
        webhook_url=mocked_webhook_url,
        error_message_format_helper=error_message_format_helper,
    )

    # when
    await slack_client.report(message_builder_option=message_builder_option)

    # then
    mock_session.post.assert_called_once()

    mock_logger.error.assert_not_called()
    mock_logger.info.assert_called_once()

@pytest.mark.asyncio
@patch("error_reporter.core.slack_client.logger")
@patch("error_reporter.core.slack_client.aiohttp.ClientSession")
async def test_slack_client_report_return_400_error(
    mock_session_class: MagicMock,
    mock_logger: MagicMock,
    slack_client: SlackClient,
    error_message_format_helper: MagicMock,
    message_builder_option: MessageBuilderOption,
    mocked_webhook_url: str,
    mocked_message: str,
) -> None:
    # given
    mock_response = AsyncMock()
    mock_response.status = 400

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    slack_client = SlackClient(
        webhook_url=mocked_webhook_url,
        error_message_format_helper=error_message_format_helper,
    )

    # when
    await slack_client.report(message_builder_option=message_builder_option)

    # then
    mock_session.post.assert_called_once()

    mock_logger.info.assert_not_called()
    mock_logger.error.assert_called_once()

@pytest.mark.asyncio
@patch("error_reporter.core.slack_client.logger")
@patch("error_reporter.core.slack_client.aiohttp.ClientSession")
async def test_slack_client_report_raised_exception(
    mock_session_class: MagicMock,
    mock_logger: MagicMock,
    slack_client: SlackClient,
    error_message_format_helper: MagicMock,
    message_builder_option: MessageBuilderOption,
    mocked_webhook_url: str,
    mocked_message: str,
) -> None:
    # given
    mock_response = AsyncMock()
    mock_response.status = 400

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.side_effect = Exception("network error")

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    slack_client = SlackClient(
        webhook_url=mocked_webhook_url,
        error_message_format_helper=error_message_format_helper,
    )

    # when
    await slack_client.report(message_builder_option=message_builder_option)

    # then
    mock_session.post.assert_called_once()

    mock_logger.info.assert_not_called()
    mock_logger.error.assert_called_once()