from typing import Optional, Any, Union, List, Dict
from datetime import datetime

from ..utils.request_builder import RequestBuilder
from ..utils.schemas import PaymentScheme, PaymentTestWebhookScheme
from ..utils.enums import (
    Network,
    Currency,
    PaymentStatus,
    Lifetime
)
from ..utils.data_classes import (
    Payment,
    Service,
    ServiceLimit,
    ServiceCommission,
    Discount,
    PaymentConvert
)


class PaymentService:
    def __init__(self, request_builder: RequestBuilder):
        self.__request_builder = request_builder

    async def test_webhook(self,
                           url_callback: str,
                           currency: Union[Currency, str],
                           network: Union[Network, str],
                           status: PaymentStatus = PaymentStatus.PAID,
                           uuid: Optional[str] = None,
                           order_id: Optional[str] = None,
                           ) -> List:
        req_data = {
            "url_callback": url_callback,
            "currency": currency,
            "network": network,
            "uuid": uuid,
            "status": status,
            "order_id": order_id
        }
        PaymentTestWebhookScheme.model_validate(req_data)
        data = (await self.__request_builder.post(
            url="https://api.heleket.com/v1/test-webhook/payment",
            data=req_data
        )).json

        return data.get("result")

    async def create_invoice(self,
                             amount: str,
                             currency: Union[Currency, str],
                             order_id: str,
                             lifetime_sec: Optional[int] = Lifetime.HOUR_1,
                             network: Optional[Union[Network, str]] = None,
                             url_callback: Optional[str] = None,
                             **kwargs
                             ) -> Payment:
        req_data = {
            "amount": amount,
            "currency": currency,
            "order_id": order_id,
            "lifetime": lifetime_sec,
            "network": network,
            "url_callback": url_callback,
            **kwargs
        }
        PaymentScheme.model_validate(req_data)
        res = await self.__request_builder.post(url="https://api.heleket.com/v1/payment", data=req_data)
        data = res.json

        result = data.get("result")
        convert_data = result.get("convert", None)
        if convert_data is not None:
            convert_data = PaymentConvert(**convert_data)
            result.pop("convert")

        from_data = result.pop("from")
        created_at_data = result.pop("created_at")
        updated_at_data = result.pop("updated_at")

        return Payment(
            from_=from_data,
            convert=convert_data,
            updated_at=datetime.fromisoformat(updated_at_data),
            created_at=datetime.fromisoformat(created_at_data),
            **result
        )

    async def info(self, uuid: Union[str, None] = None, order_id: Union[str, None] = None) -> Payment:
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")
        if uuid is not None and order_id is not None:
            raise ValueError("One of the parameters must be passed: uuid or order_id")

        data = (await self.__request_builder.post(
            url="https://api.heleket.com/v1/payment/info",
            data={
                "uuid": uuid,
                "order_id": order_id
            }
        )).json

        result = data.get("result")
        convert_data = result.get("convert", None)
        if convert_data is not None:
            convert_data = PaymentConvert(**convert_data)
            result.pop("convert")

        from_data = result.pop("from")
        created_at_data = result.pop("created_at")
        updated_at_data = result.pop("updated_at")

        return Payment(
            from_=from_data,
            convert=convert_data,
            updated_at=datetime.fromisoformat(updated_at_data),
            created_at=datetime.fromisoformat(created_at_data),
            **result
        )

    async def generate_qr_code(self, payment_uuid: str) -> str:
        data = (await self.__request_builder.post(
            url="https://api.heleket.com/v1/payment/qr",
            data={
                "merchant_payment_uuid": payment_uuid
            }
        )).json

        return data.get("result").get("image")

    async def refund(self,
                     refund_address: str,
                     is_subtract: bool,
                     uuid: Union[str, None] = None,
                     order_id: Union[str, None] = None,
                     amount: Union[int, None] = None
                     ) -> Dict[str, Any]:
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")
        if uuid is not None and order_id is not None:
            raise ValueError("one of the parameters must be passed: uuid or order_id")

        res = await self.__request_builder.post(
            url="https://api.heleket.com/v1/payment/refund",
            data={
                "address": refund_address,
                "is_subtract": is_subtract,
                "uuid": uuid,
                "order_id": order_id,
                "amount": amount
            }
        )

        return res.json.get("result")

    async def services_info(self) -> List[Service]:
        res = await self.__request_builder.post(url="https://api.heleket.com/v1/payment/services")

        serv_list = []
        for srvc in res.json.get("result"):
            limit = ServiceLimit(**srvc.pop("limit"))
            commission = ServiceCommission(**srvc.pop("commission"))
            serv_list.append(Service(**srvc, limit=limit, commission=commission))

        return serv_list

    async def discount_list(self) -> List[Discount]:
        res = await self.__request_builder.post(url="https://api.heleket.com/v1/payment/discount/list")
        return [Discount(**disc) for disc in res.json.get("result")]

    async def set_discount(self, currency: Union[Currency, str], network: Union[Network, str], discount_percent: int) -> Discount:
        data = (await self.__request_builder.post(
            url="https://api.heleket.com/v1/payment/discount/set",
            data={
                "network": network,
                "currency": currency,
                "discount_percent": discount_percent
            }
        )).json

        return Discount(**data.get("result"))

