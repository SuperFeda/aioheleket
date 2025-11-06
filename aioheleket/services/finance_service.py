from typing import Sequence, Tuple, List, Optional, Union

from ..utils.request_builder import RequestBuilder
from ..utils.enums import Currency
from ..utils.data_classes import Course, Balance


class FinanceService:
    def __init__(self, request_builder: RequestBuilder):
        self.__request_builder = request_builder

    async def exchange_rate(self, from_currency: Currency, to_currency: Optional[Sequence[Union[Currency, str]]] = None) -> List[Course]:
        res = await self.__request_builder.get(url=f"https://api.heleket.com/v1/exchange-rate/{from_currency}/list")
        result = res.json.get("result")

        courses_list = []
        if to_currency is None:
            for crs in result:
                courses_list.append(Course(from_=crs.pop("from"), **crs))
        elif to_currency is not None:
            for crs in result:
                if crs.get("to") in to_currency:
                    courses_list.append(Course(from_=crs.pop("from"), **crs))

        return courses_list

    async def balance(self) -> Tuple[List[Balance], List[Balance]]:
        data = (await self.__request_builder.post(url="https://api.heleket.com/v1/balance")).json

        all_balance = data.get("result")[0].get("balance")
        merchant_balance = [Balance(**blc) for blc in all_balance.get("merchant")]
        user_balance = [Balance(**blc) for blc in all_balance.get("user")]

        return merchant_balance, user_balance
