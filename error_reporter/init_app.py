from fastapi import FastAPI

from error_reporter.core.core_client import CoreClient
from error_reporter.service.error_reporter_filter import error_reporter_filter
from error_reporter.service.error_reporter_service_container import get_client
from error_reporter.types.error_reporter_options import ErrorReporterOptions

core_client: CoreClient

def init_error_reporter(app: FastAPI, options: ErrorReporterOptions):
    app.state.error_reporter_client = get_client(options)
    app.middleware('http')(error_reporter_filter)