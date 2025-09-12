from typing import Optional, Union, List

from ..utils.request_builder import RequestBuilder
from ..utils.enums import (
    Network,
    Currency,
    CourseSource,
    Priority
)
from ..utils.schemas import PayoutScheme
from ..utils.data_classes import (
    Service,
    ServiceCommission,
    ServiceLimit,
    Payout,
    Transfer,
    PayoutConvert, PayoutSum
)


class PayoutService:
    def __init__(self, request_builder: RequestBuilder):
        self.__request_builder = request_builder

    async def create_invoice(self,
                             amount: str,
                             currency: Currency,
                             order_id: str,
                             address: str,
                             is_subtract: bool,
                             network: Network,
                             **kwargs
                             ) -> Payout:
        req_data = {
            "amount": amount,
            "currency": currency,
            "order_id": order_id,
            "address": address,
            "is_subtract": is_subtract,
            "network": network,
            **kwargs
        }
        PayoutScheme.model_validate(req_data)
        res = await self.__request_builder.post(url="https://api.heleket.com/v1/payout", data=req_data)
        data = res.json

        convert_data = data.get("result").get("convert", None)
        if convert_data is not None:
            convert_data = PayoutConvert(**convert_data)
            data.get("result").pop("convert")

        return Payout(convert=convert_data, **data)

    async def calc(self,
                   amount: str,
                   address: str,
                   currency: Currency,
                   is_subtract: bool,
                   to_currency: Optional[str],
                   network: Optional[Network],
                   course_source: Optional[CourseSource],
                   priority: Optional[Priority]
                   ) -> PayoutSum:
        data = (await self.__request_builder.post(
            url="https://api.heleket.com/v1/payout/calc",
            data={
                "amount": amount,
                "address": address,
                "currency": currency,
                "is_subtract": is_subtract,
                "to_currency": to_currency,
                "network": network,
                "course_source": course_source,
                "priority": priority
            }
        )).json

        return PayoutSum(**data.get("result"))

    async def personal_transfer(self, amount: str, currency: Currency) -> Transfer:
        data = (await self.__request_builder.post(
            url="https://api.heleket.com/v1/transfer/to-personal",
            data={"amount": amount, "currency": currency}
        )).json

        return Transfer(**data.get("result"))

    async def business_transfer(self, amount: str, currency: Currency) -> Transfer:
        data = (await self.__request_builder.post(
            url="https://api.heleket.com/v1/transfer/to-business",
            data={"amount": amount, "currency": currency}
        )).json

        return Transfer(**data.get("result"))

    async def get_info(self, uuid: Union[str, None] = None, order_id: Union[str, None] = None) -> Payout:
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")
        if uuid is not None and order_id is not None:
            raise ValueError("one of the parameters must be passed: uuid or order_id")

        res = await self.__request_builder.post(
            url="https://api.heleket.com/v1/payout/info",
            data={"uuid": uuid, "order_id": order_id}
        )
        data = res.json

        return Payout(**data.get("result"))

    async def get_services(self) -> List[Service]:
        res = await self.__request_builder.post(url="https://api.heleket.com/v1/payout/services")

        serv_list = []
        for srvc in res.json.get("result"):
            limit = ServiceLimit(**srvc.get("limit"))
            commission = ServiceCommission(**srvc.get("commission"))
            srvc.pop("limit")
            srvc.pop("commission")
            serv_list.append(Service(**srvc, limit=limit, commission=commission))

        return serv_list


