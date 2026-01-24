from typing import Sequence, List, Optional, Union, Dict, Any

from .base_service import _BaseService
from ..utils.request_builder import RequestBuilder
from ..enums import CryptoCurrency
from ..data_classes import Course, Balance, CurrencyBalance
from ..types.aliases import Currency


class FinanceService(_BaseService):
    def __init__(self, request_builder: RequestBuilder):
        super().__init__(request_builder=request_builder)

    async def exchange_rate(self,
                            from_currency: Union[CryptoCurrency, str],
                            to_currency: Optional[Sequence[Currency]] = None
                            ) -> List[Course]:
        """
        Retrieves current exchange rates for the specified currency.

        :param from_currency: The base currency for which exchange rates are requested.
        :param to_currency: List of target currencies to get exchange rates for. If not specified (None), returns all available rates for the base currency.

        :return: List of Course objects containing exchange rate information.
        """
        result = await self._get_result_data("GET", f"/exchange-rate/{from_currency}/list")
        if to_currency:
            return [self.__create_currency_course(crs) for crs in result if crs.get("to") in to_currency]
        return [self.__create_currency_course(crs) for crs in result]

    @staticmethod
    def __create_currency_course(currency_course_info: Dict[str, Any]) -> Course:
        return Course(from_=currency_course_info.pop("from"), **currency_course_info)

    async def balance(self) -> Balance:
        """
        Get user and merchant balance
        """
        result = await self._get_result_data("POST", "/balance")
        balance_data = result[0].get("balance")
        merchant_balance = await self.__get_entity_balance(balance_data.get("merchant"))
        user_balance = await self.__get_entity_balance(balance_data.get("user"))
        return Balance(merchant=merchant_balance, user=user_balance)

    @staticmethod
    async def __get_entity_balance(all_entity_balance_info: List[Dict[str, Any]]) -> List[CurrencyBalance]:
        return [
            CurrencyBalance(
                currency_code=b.get("currency_code"),
                crypto_amount=b.get("balance"),
                usd_amount=b.get("balance_usd"),
                uuid=b.get("uuid")
            ) for b in all_entity_balance_info
        ]
