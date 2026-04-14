import httpx
import certifi
from abc import ABC, abstractmethod

class CoreClient(ABC):
    _client: httpx.AsyncClient = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(verify=certifi.where())
        return self._client

    @abstractmethod
    async def report(self, message_builder_option):
        ...