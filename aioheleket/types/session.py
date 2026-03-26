from aiohttp import ClientSession, ClientTimeout, TCPConnector

from aioheleket.data_classes import RequestConfig


class Session:
    def __init__(self, config: RequestConfig):
        self._session = None
        self._config = config

    async def create_new_if_none(self) -> None:
        if self._session is None:
            timeout = ClientTimeout(total=self._config.timeout_s)
            connector = TCPConnector(
                limit=self._config.connector_limit,
                limit_per_host=self._config.connector_limit_per_host,
                ttl_dns_cache=self._config.ttl_dns_cache,
                enable_cleanup_closed=True,
            )
            self._session = ClientSession(timeout=timeout, connector=connector)

    async def close(self) -> None:
        if self._session is None:
            raise RuntimeError("Session is not initialized")
        await self._session.close()

    async def get(self) -> ClientSession:
        return self._session
