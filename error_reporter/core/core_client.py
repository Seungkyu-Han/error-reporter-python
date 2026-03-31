from abc import ABC, abstractmethod

from error_reporter.core.helper.error_message_format_helper import ErrorMessageFormatHelper
from error_reporter.types.message_builder_option import MessageBuilderOption


class CoreClient(ABC):
    _error_message_format_helper: ErrorMessageFormatHelper

    @abstractmethod
    async def report(self, message_builder_option: MessageBuilderOption):
        ...
