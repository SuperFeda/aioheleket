from typing import Sequence, List, Optional

from .base_service import _BaseService
from aioheleket.request_builder import RequestBuilder
from aioheleket.validation.schemas import Course, Balance
from aioheleket.types.aliases import Currency, CryptoCurrencyStr


class FinanceService(_BaseService):
    def __init__(self, request_builder: RequestBuilder):
        super().__init__(request_builder=request_builder)

    async def exchange_rate(self,
                            from_currency: CryptoCurrencyStr,
                            to_currency: Optional[Sequence[Currency]] = None
                            ) -> List[Course]:
        """
        Retrieves current exchange rates for the specified currency.

        doc https://doc.heleket.com/en/other/list-of-exchange-rates

        :param from_currency: The base currency for which exchange rates are requested.
        :param to_currency: List of target currencies to get exchange rates for. If not specified (None), returns all available rates for the base currency.

        :return: List of Course objects containing exchange rate information.
        """
        result = await self._get_result_data("GET", f"/exchange-rate/{from_currency}/list")
        if to_currency:
            return [Course.model_validate(crs) for crs in result if crs.get("to") in to_currency]
        return [Course.model_validate(crs) for crs in result]

    async def balance(self) -> Balance:
        """
        Get user and merchant balance

        doc https://doc.heleket.com/en/other/balance
        """
        result = await self._get_result_data("POST", "/balance")
        balance_data = result[0].get("balance")
        return Balance.model_validate(balance_data)

