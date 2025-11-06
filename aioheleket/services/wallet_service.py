from typing import Optional, Union, Tuple

from ..utils.request_builder import RequestBuilder
from ..utils.enums import Network, Currency, StaticWalletStatus
from ..utils.schemas import WalletScheme
from ..utils.data_classes import Wallet


class StaticWalletService:
    def __init__(self, request_builder: RequestBuilder):
        self.__request_builder = request_builder

    async def create(self,
                     currency: Union[Currency, str],
                     network: Union[Network, str],
                     order_id: str,
                     url_callback: Optional[str] = None,
                     from_referral_code: Optional[str] = None
                     ) -> Wallet:
        req_data = {
            "currency": currency,
            "order_id": order_id,
            "network": network,
            "url_callback": url_callback,
            "from_referral_code": from_referral_code
        }
        WalletScheme.model_validate(req_data)
        res = await self.__request_builder.post(url="https://api.heleket.com/v1/wallet", data=req_data)
        return Wallet(**res.json.get("result"))

    async def block(self,
                    uuid: Union[str, None] = None,
                    order_id: Union[str, None] = None,
                    is_force_refund: bool = False
                    ) -> Tuple[str, StaticWalletStatus]:
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")
        if uuid is not None and order_id is not None:
            raise ValueError("one of the parameters must be passed: uuid or order_id")

        res = await self.__request_builder.post(
            url="https://api.heleket.com/v1/wallet/block-address",
            data={
                "uuid": uuid,
                "order_id": order_id,
                "is_force_refund": is_force_refund
            }
        )
        data = res.json

        return data.get("result").get("uuid"), data.get("result").get("status")

    async def generate_qr_code(self, wallet_uuid: str) -> str:
        data = (await self.__request_builder.post(
            url="https://api.heleket.com/v1/wallet/qr",
            data={"wallet_address_uuid": wallet_uuid}
        )).json

        return data.get("result").get("image")

    async def blocked_address_refund(self,
                                     refund_address: str,
                                     uuid: Union[str, None] = None,
                                     order_id: Union[str, None] = None
                                     ) -> Tuple[str, str]:
        if uuid is None and order_id is None:
            raise ValueError("Required parameter not passed: uuid or order_id")
        if uuid is not None and order_id is not None:
            raise ValueError("one of the parameters must be passed: uuid or order_id")

        res = await self.__request_builder.post(
            url="https://api.heleket.com/v1/wallet/blocked-address-refund",
            data={
                "uuid": uuid,
                "order_id": order_id,
                "address": refund_address
            }
        )
        data = res.json

        return data.get("result").get("commission"), data.get("result").get("amount")

