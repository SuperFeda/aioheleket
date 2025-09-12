from aiohttp import ClientSession
from typing import Union

from ..services import PayoutService
from ..services import PaymentService
from ..services import StaticWalletService
from ..services import FinanceService
from ..utils.request_builder import RequestBuilder


class HeleketClient:
    def __init__(self,
                 merchant_id: str,
                 payment_api_key: Union[str, None] = None,
                 payout_api_key: Union[str, None] = None,
                 ) -> None:
        if not merchant_id:
            raise ValueError("Merchant id is empty")

        self.__merchant_id = merchant_id
        self.__payment_api_key = payment_api_key
        self.__payout_api_key = payout_api_key
        self.__session = None

    async def payment(self) -> PaymentService:
        if not self.__payment_api_key:
            raise ValueError("Payment API key is empty")

        return PaymentService(RequestBuilder(
            merchant_id=self.__merchant_id,
            api_key=self.__payment_api_key,
            session=await self.__create_session()
        ))

    async def payout(self) -> PayoutService:
        if not self.__payout_api_key:
            raise ValueError("Payout API key is empty")

        return PayoutService(RequestBuilder(
            merchant_id=self.__merchant_id,
            api_key=self.__payout_api_key,
            session=await self.__create_session()
        ))

    async def static_wallet(self) -> StaticWalletService:
        if not self.__payment_api_key:
            raise ValueError("Payment API key is empty")

        return StaticWalletService(RequestBuilder(
            merchant_id=self.__merchant_id,
            api_key=self.__payment_api_key,
            session=await self.__create_session()
        ))

    async def finance(self) -> FinanceService:
        if not self.__payment_api_key:
            raise ValueError("Payment API key is empty")

        return FinanceService(RequestBuilder(
            merchant_id=self.__merchant_id,
            api_key=self.__payment_api_key,
            session=await self.__create_session()
        ))

    async def __create_session(self) -> ClientSession:
        if self.__session is None:
            self.__session = ClientSession()
        return self.__session

    async def close_session(self) -> None:
        if self.__session is None:
            raise RuntimeError("Session is not initialized")
        await self.__session.close()
