from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException, status
from starlette.responses import Response

from error_reporter.service.error_reporter_filter import error_reporter_filter


@pytest.mark.asyncio
async def test_filter_without_client():
    # given
    request = MagicMock()
    request.app.state.error_reporter_client = None

    call_next = AsyncMock(return_value=Response(status_code=200))

    # when
    response = await error_reporter_filter(request, call_next)

    # then
    assert response.status_code == 200
    call_next.assert_called_once()


@pytest.mark.asyncio
async def test_filter_success():
    # given
    request = MagicMock()
    client = AsyncMock()
    request.app.state.error_reporter_client = client

    call_next = AsyncMock(return_value=Response(status_code=200))

    # when
    response = await error_reporter_filter(request, call_next)

    # then
    assert response.status_code == 200
    call_next.assert_called_once()
    client.report.assert_not_called()


@pytest.mark.asyncio
async def test_filter_http_exception():
    # given
    request = MagicMock()
    client = AsyncMock()
    request.app.state.error_reporter_client = client

    async def raise_http_exception(req):
        raise HTTPException(status_code=400)

    # when & then
    with pytest.raises(HTTPException):
        await error_reporter_filter(request, raise_http_exception)

    client.report.assert_not_called()


@pytest.mark.asyncio
async def test_filter_general_exception():
    # given
    request = MagicMock()
    client = AsyncMock()
    request.app.state.error_reporter_client = client

    request.method = "GET"
    request.url.path = "/test"
    request.headers = {}
    request.client.host = "127.0.0.1"
    request.body = AsyncMock(return_value=b"test-body")

    async def raise_exception(req):
        raise Exception("boom")

    # when
    response = await error_reporter_filter(request, raise_exception)

    # then
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    client.report.assert_called_once()

    # message_builder_option 검증
    args, kwargs = client.report.call_args
    mbo = kwargs["message_builder_option"]

    assert mbo.method == "GET"
    assert mbo.path == "/test"
    assert mbo.ip == "127.0.0.1"
    assert mbo.body == "test-body"
    assert mbo.error == "boom"
    assert "Exception" in mbo.stack

@pytest.mark.asyncio
async def test_filter_no_x_forwarded_for():
    # given
    request = MagicMock()
    client = AsyncMock()
    request.app.state.error_reporter_client = client

    request.method = "GET"
    request.url.path = "/test"
    request.headers = {}
    request.client.host = "127.0.0.1"
    request.body = AsyncMock(return_value=b"")

    async def raise_exception(req):
        raise Exception("boom")

    # when
    await error_reporter_filter(request, raise_exception)

    # then
    args, kwargs = client.report.call_args
    mbo = kwargs["message_builder_option"]

    assert mbo.ip == "127.0.0.1"

@pytest.mark.asyncio
async def test_filter_x_forwarded_for():
    # given
    request = MagicMock()
    client = AsyncMock()
    request.app.state.error_reporter_client = client

    request.method = "GET"
    request.url.path = "/test"
    request.headers = {"x-forwarded-for": "1.2.3.4, 5.6.7.8"}
    request.client.host = "127.0.0.1"
    request.body = AsyncMock(return_value=b"")

    async def raise_exception(req):
        raise Exception("boom")

    # when
    await error_reporter_filter(request, raise_exception)

    # then
    args, kwargs = client.report.call_args
    mbo = kwargs["message_builder_option"]

    assert mbo.ip == "1.2.3.4"