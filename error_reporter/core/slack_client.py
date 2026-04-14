import logging

from error_reporter.core.core_client import CoreClient
from error_reporter.core.error_message_format_helper import ErrorMessageFormatHelper
from error_reporter.types.message_builder_option import MessageBuilderOption

logger = logging.getLogger(__name__)


class SlackClient(CoreClient):

    def __init__(self, webhook_url: str, error_message_format_helper: ErrorMessageFormatHelper):
        self._webhook_url = webhook_url
        self._error_message_format_helper = error_message_format_helper
        self._logger = logging.getLogger(self.__class__.__name__)

    async def report(self, message_builder_option: MessageBuilderOption):
        send_message: str = self._error_message_format_helper.error_message(
            message_builder_option=message_builder_option)

        try:
            client = await self._get_client()

            response = await client.post(
                self._webhook_url,
                json={"text": send_message},
                headers={"Content-Type": "application/json"}
            )

            if response.is_success:
                self._logger.info("error_reporter send error success")
            else:
                self._logger.error("slack send failed: status=%s", response.status_code)

        except Exception as ex:
            logger.error(f"error reporter fail to send: {ex}")
