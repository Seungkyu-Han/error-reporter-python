from unittest.mock import MagicMock, patch
from fastapi import FastAPI

from error_reporter import init_error_reporter


@patch("error_reporter.init_app.get_client")
def test_init_error_reporter(mock_get_client):
    # given
    app = FastAPI()
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    options = MagicMock()

    # when
    init_error_reporter(app, options)

    # then
    assert app.state.error_reporter_client == mock_client
    mock_get_client.assert_called_once_with(options)