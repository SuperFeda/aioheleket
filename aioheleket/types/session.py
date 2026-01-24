from aiohttp import ClientSession


class Session:
    def __init__(self):
        self._session = None

    async def create_new_if_none(self) -> None:
        if self._session is None:
            self._session = ClientSession()

    async def close(self) -> bool:
        if self._session is None:
            raise RuntimeError("Session is not initialized")
        await self._session.close()
        return True

    async def get(self) -> ClientSession:
        return self._session
