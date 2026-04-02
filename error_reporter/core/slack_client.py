import logging
import aiohttp
import ssl
import certifi

from error_reporter.core.core_client import CoreClient
from error_reporter.core.error_message_format_helper import ErrorMessageFormatHelper
from error_reporter.types.message_builder_option import MessageBuilderOption

logger = logging.getLogger(__name__)


class SlackClient(CoreClient):

    def __init__(self, webhook_url: str, error_message_format_helper: ErrorMessageFormatHelper):
        self._webhook_url = webhook_url
        self._error_message_format_helper = error_message_format_helper
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())

    async def report(self, message_builder_option: MessageBuilderOption):
        send_message: str = self._error_message_format_helper.error_message(
            message_builder_option=message_builder_option)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        self._webhook_url,
                        json={"text": send_message},
                        headers={"content-Type": "application/json"}
                ) as response:
                    if 200 <= response.status < 300:
                        logger.info("error_reporter send error success")
                    elif response.status >= 400:
                        logger.error("Slack send failed: status=%s", response.status)

        except Exception as ex:
            logger.error(f"error reporter fail to send: {ex}")
