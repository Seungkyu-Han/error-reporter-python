from unittest.mock import patch, MagicMock

from error_reporter.core.error_message_format_helper import ErrorMessageFormatHelper
from error_reporter.types.message_builder_option import MessageBuilderOption


def test_error_message_format_helper_correctly():
    ErrorMessageFormatHelper(server_name='')


def test_error_message_format_helper_without_server_name():
    ErrorMessageFormatHelper()


def test_create_error_message_correctly():
    # given
    server_name = "test server name"
    method = "test method"
    path = "test path"
    ip = "test ip"
    body = """ { "name": "seungkyu" }  """
    error = "test error"
    stack = "test stack"

    message_builder_option = MessageBuilderOption(
        method=method,
        path=path,
        ip=ip,
        body=body,
        error=error,
        stack=stack,
    )

    error_message_format_helper = ErrorMessageFormatHelper(server_name=server_name)

    # when
    error_message = error_message_format_helper.error_message(message_builder_option=message_builder_option)

    # then
    assert server_name in error_message
    assert method in error_message
    assert path in error_message
    assert ip in error_message
    assert "seungkyu" in error_message
    assert error in error_message
    assert stack in error_message


def test_create_error_message_not_json():
    # given
    server_name = "test server name"
    method = "test method"
    path = "test path"
    ip = "test ip"
    body = """ test """
    error = "test error"
    stack = "test stack"

    message_builder_option = MessageBuilderOption(
        method=method,
        path=path,
        ip=ip,
        body=body,
        error=error,
        stack=stack,
    )

    error_message_format_helper = ErrorMessageFormatHelper(server_name=server_name)

    # when
    error_message = error_message_format_helper.error_message(message_builder_option=message_builder_option)

    # then
    assert 'test' in error_message


@patch("error_reporter.core.error_message_format_helper.json")
def test_create_error_message_exception(mock_json_class: MagicMock):
    # given
    server_name = "test_server_name"

    message_builder_option = MessageBuilderOption()

    error_message_format_helper = ErrorMessageFormatHelper(server_name=server_name)

    mock_json_class.dumps.side_effect = Exception("Serialization Error")

    # when
    error_message = error_message_format_helper.error_message(message_builder_option=message_builder_option)

    # then
    assert 'None (Serialization Failed)' in error_message
