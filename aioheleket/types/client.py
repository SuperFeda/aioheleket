from aiohttp import ClientSession
from typing import Union, Type, Optional

from .session import Session
from aioheleket.services import (
    PaymentService,
    PayoutService,
    StaticWalletService,
    FinanceService
)
from aioheleket.data_classes import RequestConfig
from aioheleket.request_builder import RequestBuilder

PaymentKeyServices = Union[PaymentService, StaticWalletService, FinanceService]
PayoutKeyServices = Union[PayoutService]


class HeleketClient:
    """
    Base client for interacting with the Heleket API.

    This class provides access to specialized services, each handling a specific Heleket entity. Available services include payments, payouts, static wallets, and finance (for exchange rates and balances).

    Initialize the class with a mandatory merchant_id. Note that each service requires its corresponding API key:
        - payment_service(), static_wallet_service(), finance_service() => payment_api_key
        - payout_service() => payout_api_key
    """

    def __init__(self,
                 merchant_id: str,
                 payment_api_key: Union[str, None] = None,
                 payout_api_key: Union[str, None] = None,
                 config: Optional[RequestConfig] = None
                 ) -> None:
        if not merchant_id:
            raise ValueError("Merchant ID is empty")

        self.__merchant_id = merchant_id
        self.__payment_api_key = payment_api_key
        self.__payout_api_key = payout_api_key

        self._payment_request_builder = None
        self._payout_request_builder = None

        self._config = config or RequestConfig()
        self._session = Session(self._config)

        self._payment_service = None
        self._payout_service = None
        self._static_wallet_service = None
        self._finance_service = None

    async def __aenter__(self) -> "HeleketClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close_session()

    async def payment_service(self) -> PaymentService:
        """Getting payment service"""
        if self._payment_service is None:
            service = await self.__create_service_with_payment_key(PaymentService)
            self._payment_service = service
        return self._payment_service

    async def payout_service(self) -> PayoutService:
        """Getting payout service"""
        if self._payout_service is None:
            service = await self.__create_service_with_payout_key(PayoutService)
            self._payout_service = service
        return self._payout_service

    async def static_wallet_service(self) -> StaticWalletService:
        """Getting static wallet service"""
        if self._static_wallet_service is None:
            service = await self.__create_service_with_payment_key(StaticWalletService)
            self._static_wallet_service = service
        return self._static_wallet_service

    async def finance_service(self) -> FinanceService:
        """Getting finance service"""
        if self._finance_service is None:
            service = await self.__create_service_with_payment_key(FinanceService)
            self._finance_service = service
        return self._finance_service

    async def __create_service_with_payment_key(self, service: Type[PaymentKeyServices]) -> PaymentKeyServices:
        if not self.__payment_api_key:
            raise ValueError("Payment API key is empty")
        if not self._payment_request_builder:
            self._payment_request_builder = RequestBuilder(
                merchant_id=self.__merchant_id,
                api_key=self.__payment_api_key,
                session=await self.__create_session(),
                config=self._config
            )
        return service(self._payment_request_builder)

    async def __create_service_with_payout_key(self, service: Type[PayoutKeyServices]) -> PayoutKeyServices:
        if not self.__payout_api_key:
            raise ValueError("Payout API key is empty")
        if not self._payout_request_builder:
            self._payout_request_builder = RequestBuilder(
                merchant_id=self.__merchant_id,
                api_key=self.__payout_api_key,
                session=await self.__create_session(),
                config=self._config
            )
        return service(self._payout_request_builder)

    async def __create_session(self) -> ClientSession:
        await self._session.create_new_if_none()
        return await self._session.get()

    async def close_session(self) -> None:
        await self._session.close()
