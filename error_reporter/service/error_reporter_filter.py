import traceback

from fastapi import Request, Response, HTTPException, status

from error_reporter.core.core_client import CoreClient
from error_reporter.types.message_builder_option import MessageBuilderOption


async def error_reporter_filter(request: Request, call_next):
    client: CoreClient = request.app.state.error_reporter_client

    if client is None:
        return await call_next(request)

    try:
        return await call_next(request)

    except HTTPException:
        raise

    except Exception as exception:

        method: str = request.method
        path: str = str(request.url)

        x_forwarded_for = request.headers.get("x-forwarded-for")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.client.host



        error = str(exception)

        stack = traceback.format_exc()

        message_builder_option = MessageBuilderOption(
            method=method,
            path=path,
            ip=ip,
            error=error,
            stack=stack
        )

        await client.report(message_builder_option=message_builder_option)

        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error"
        )
