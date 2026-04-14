import logging

from error_reporter.core.core_client import CoreClient
from error_reporter.core.error_message_format_helper import ErrorMessageFormatHelper
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

        client = await self._get_client()

        response = await client.get(
            url,
            headers=headers,
        )

        if not response.is_success:
            if response.status_code == 404:
                raise Exception("GitHub Not Found: Invalid repository or owner")
            else:
                raise Exception(f"GitHub API Error: {response.status_code}")

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

        client = await self._get_client()

        response = await client.post(
            url,
            headers=headers,
            json=payload,
        )

        if not response.is_success:

            if response.status_code == 403:
                logging.error(
                    "ErrorReporter: Insufficient permissions or rate limit exceeded, Please check your github token"
                )
            elif response.status_code == 404:
                logging.error(
                    "ErrorReporter: Invalid repository or owner"
                )
            else:
                logging.error(
                    f"ErrorReporter: {response.status_code}"
                )
