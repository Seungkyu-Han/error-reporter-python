import pytest

from unittest.mock import MagicMock, patch, AsyncMock

from error_reporter.core.github_client import GithubClient
from error_reporter.types.message_builder_option import MessageBuilderOption


@pytest.fixture
def _mock_message() -> str:
    return "mock_message"


@pytest.fixture
def _mock_github_token() -> str:
    return "mock_github_token"


@pytest.fixture
def _mock_repository() -> str:
    return "mock_repository"


@pytest.fixture
def _mock_owner() -> str:
    return "mock_owner"


@pytest.fixture
def message_builder_option() -> MessageBuilderOption:
    return MessageBuilderOption()


@pytest.fixture
def _error_message_format_helper(_mock_message: str) -> MagicMock:
    helper = MagicMock()
    helper.error_message.return_value = _mock_message
    return helper


@pytest.fixture
def github_client(
        _mock_github_token: str,
        _mock_repository: str,
        _mock_owner: str,
        _error_message_format_helper: MagicMock
) -> GithubClient:
    return GithubClient(
        github_token=_mock_github_token,
        repository=_mock_repository,
        owner=_mock_owner,
        error_message_format_helper=_error_message_format_helper
    )


def test_github_client_init_correctly(
        github_client: GithubClient
):
    assert github_client is not None
    assert github_client._error_message_format_helper is not None


@pytest.mark.asyncio
@patch("error_reporter.core.github_client.logging")
@patch("error_reporter.core.github_client.aiohttp.ClientSession")
async def test_github_client_create_correctly(
        mock_session_class: MagicMock,
        mock_logger: MagicMock,
        github_client: GithubClient,
):
    # given
    mock_response = AsyncMock()
    mock_response.status = 200

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    # when
    await github_client.create(
        github_token=github_client._github_token,
        repository=github_client._repository,
        owner=github_client._owner,
        error_message_format_helper=github_client._error_message_format_helper,
    )

    # when
    mock_session.get.assert_called_once()

    mock_logger.error.assert_not_called()


@pytest.mark.asyncio
@patch("error_reporter.core.github_client.aiohttp.ClientSession")
async def test_github_client_create_return_404_error(
        mock_session_class: MagicMock,
        github_client: GithubClient,
):
    # given
    mock_response = AsyncMock()
    mock_response.status = 404

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    # when, then
    with pytest.raises(Exception):
        await github_client.create(
            github_token=github_client._github_token,
            repository=github_client._repository,
            owner=github_client._owner,
            error_message_format_helper=github_client._error_message_format_helper,
        )

    # when
    mock_session.get.assert_called_once()

@pytest.mark.asyncio
@patch("error_reporter.core.github_client.aiohttp.ClientSession")
async def test_github_client_create_return_400_error(
        mock_session_class: MagicMock,
        github_client: GithubClient,
):
    # given
    mock_response = AsyncMock()
    mock_response.status = 400

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    # when, then
    with pytest.raises(Exception):
        await github_client.create(
            github_token=github_client._github_token,
            repository=github_client._repository,
            owner=github_client._owner,
            error_message_format_helper=github_client._error_message_format_helper,
        )

    # when
    mock_session.get.assert_called_once()

@pytest.mark.asyncio
@patch("error_reporter.core.github_client.logging")
@patch("error_reporter.core.github_client.aiohttp.ClientSession")
async def test_github_client_report_correctly(
        mock_session_class: MagicMock,
        mock_logger: MagicMock,
        github_client: GithubClient,
        message_builder_option: MessageBuilderOption
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
    await github_client.report(message_builder_option=message_builder_option)

    # then
    mock_session.post.assert_called_once()

    mock_logger.assert_not_called()


@pytest.mark.asyncio
@patch("error_reporter.core.github_client.logging")
@patch("error_reporter.core.github_client.aiohttp.ClientSession")
async def test_github_client_report_return_400_error(
        mock_session_class: MagicMock,
        mock_logger: MagicMock,
        github_client: GithubClient,
        message_builder_option: MessageBuilderOption
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
    await github_client.report(message_builder_option=message_builder_option)

    # then
    mock_session.post.assert_called_once()

    mock_logger.error.assert_called_once()

@pytest.mark.asyncio
@patch("error_reporter.core.github_client.logging")
@patch("error_reporter.core.github_client.aiohttp.ClientSession")
async def test_github_client_report_return_403_error(
        mock_session_class: MagicMock,
        mock_logger: MagicMock,
        github_client: GithubClient,
        message_builder_option: MessageBuilderOption
):
    # given
    mock_response = AsyncMock()
    mock_response.status = 403

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    # when
    await github_client.report(message_builder_option=message_builder_option)

    # then
    mock_session.post.assert_called_once()

    mock_logger.error.assert_called_once()

@pytest.mark.asyncio
@patch("error_reporter.core.github_client.logging")
@patch("error_reporter.core.github_client.aiohttp.ClientSession")
async def test_github_client_report_return_404_error(
        mock_session_class: MagicMock,
        mock_logger: MagicMock,
        github_client: GithubClient,
        message_builder_option: MessageBuilderOption
):
    # given
    mock_response = AsyncMock()
    mock_response.status = 404

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.return_value = mock_response

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    # when
    await github_client.report(message_builder_option=message_builder_option)

    # then
    mock_session.post.assert_called_once()

    mock_logger.error.assert_called_once()


@pytest.mark.asyncio
@patch("error_reporter.core.github_client.logging")
@patch("error_reporter.core.github_client.aiohttp.ClientSession")
async def test_github_client_report_raised_exception(
        mock_session_class: MagicMock,
        mock_logger: MagicMock,
        github_client: GithubClient,
        message_builder_option: MessageBuilderOption
):
    # given
    mock_response = AsyncMock()
    mock_response.status = 404

    mock_post_ctx = AsyncMock()
    mock_post_ctx.__aenter__.side_effect = Exception("network error")

    mock_session = AsyncMock()
    mock_session.post = MagicMock(return_value=mock_post_ctx)

    mock_session_class.return_value.__aenter__.return_value = mock_session

    # when, then
    with pytest.raises(Exception):
        await github_client.report(message_builder_option=message_builder_option)