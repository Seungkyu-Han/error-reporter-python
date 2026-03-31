import logging
import ssl
import aiohttp
import certifi

from error_reporter.core.core_client import CoreClient
from error_reporter.core.helper.error_message_format_helper import ErrorMessageFormatHelper
from error_reporter.types.message_builder_option import MessageBuilderOption


class GithubClient(CoreClient):

    def __init__(
            self,
            github_token: str,
            repository: str,
            owner: str,
            error_message_format_helper: ErrorMessageFormatHelper,
    ):
        self._github_token = github_token
        self._repository = repository
        self._owner = owner
        self._error_message_format_helper = error_message_format_helper
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())

    @classmethod
    async def create(
            cls,
            github_token: str,
            repository: str,
            owner: str,
            error_message_format_helper: ErrorMessageFormatHelper,
    ):
        self = cls(github_token, repository, owner, error_message_format_helper)
        await self.check_github_access()
        return self

    async def check_github_access(self):
        url = f"https://api.github.com/repos/{self._owner}/{self._repository}/issues"

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._github_token}",
            "X-GitHub-Api-Version": "2026-03-10",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=self._ssl_context) as response:
                if response.status != 200:
                    if response.status == 404:
                        raise Exception("GitHub Not Found: Invalid repository or owner")
                    else:
                        raise Exception(f"GitHub API Error: {response.status}")

    async def report(self, message_builder_option: MessageBuilderOption):
        url = f"https://api.github.com/repos/{self._owner}/{self._repository}/issues"

        title = f"[FIX] {message_builder_option.error}"
        body = self._error_message_format_helper.error_message(message_builder_option)

        headers = {
            "Authorization": f"Bearer {self._github_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "title": title,
            "body": body,
            "labels": ["bug"],
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url,
                        headers=headers,
                        json=payload,
                        ssl=self._ssl_context,
                ) as response:

                    if response.status >= 400:
                        error_body = await response.text()

                        if response.status == 403:
                            logging.error(
                                "ErrorReporter: Insufficient permissions or rate limit exceeded, Please check your github token"
                            )
                        elif response.status == 404:
                            logging.error(
                                "ErrorReporter: Invalid repository or owner"
                            )
                        else:
                            logging.error(
                                f"ErrorReporter: {response.status}: {error_body}"
                            )

        except Exception as error:
            raise error
