from typing import Union
from fastapi import FastAPI

from error_reporter.service.error_reporter_filter import error_reporter_filter
from error_reporter.service.error_reporter_service_container import get_client
from .error_reporter_options import SlackOptions, DiscordOptions


def init_error_reporter(app: FastAPI, options: Union[SlackOptions, DiscordOptions]):
    setattr(app.state, 'error_reporter_client', get_client(options)) # type: ignore[attr-defined]
    app.middleware('http')(error_reporter_filter)