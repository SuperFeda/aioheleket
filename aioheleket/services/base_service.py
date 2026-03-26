from datetime import datetime
from typing import Dict, Any, Optional, Union, List

from aioheleket.data_classes import Response
from aioheleket.enums import PaymentStatus, PayoutStatus, StaticWalletStatus
from aioheleket.request_builder import RequestBuilder
from aioheleket.validation.schemas import TestWebhook, Service
from aioheleket.types.aliases import HttpMethod, CryptoCurrencyStr, NetworkStr


class _BaseService:
    def __init__(self, request_builder: RequestBuilder):
        self._request_builder = request_builder

    async def _create_request(self,
                              method: HttpMethod,
                              endpoint: str,
                              data: Optional[Dict[str, Any]] = None
                              ) -> Response:
        if method not in ("POST", "GET"):
            raise ValueError("The method must be either POST or GET")

        if method == "POST":
            return await self._request_builder.post(endpoint=endpoint, data=data)
        elif method == "GET":
            return await self._request_builder.get(endpoint=endpoint)

    async def _get_result_data(self,
                               method: HttpMethod,
                               endpoint: str,
                               data: Optional[Dict[str, Any]] = None
                               ) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        response = await self._create_request(method=method, endpoint=endpoint, data=data)
        data = response.json
        result = data.get("result", None)
        return result

    async def _get_qr_image_base64(self, endpoint: str, request_data: Dict[str, str]) -> str:
        result = await self._get_result_data("POST", endpoint, request_data)
        base64_qr_image = result.get("image")
        return base64_qr_image

    async def _get_services_info(self, endpoint: str) -> List[Service]:
        result = await self._get_result_data("POST", endpoint)
        return [Service.model_validate(service) for service in result]

    async def _get_history_data(self,
                                endpoint: str,
                                date_from: Optional[datetime] = None,
                                date_to: Optional[datetime] = None
                                ):
        date_format = "%Y-%m-%d %H:%M:%S"
        request_data = {
            "data_from": date_from.strftime(date_format) if isinstance(date_from, datetime) else date_from,
            "date_to": date_to.strftime(date_format) if isinstance(date_to, datetime) else date_to
        }
        result = await self._get_result_data(method="POST", endpoint=endpoint, data=request_data)
        return result

    async def _create_test_webhook(self,
                                   endpoint: str,
                                   *,
                                   url_callback: str,
                                   currency: CryptoCurrencyStr,
                                   network: NetworkStr,
                                   status: Union[PaymentStatus, PayoutStatus, StaticWalletStatus, str],
                                   uuid: Optional[str] = None,
                                   order_id: Optional[str] = None,
                                   ) -> List:
        webhook_data = TestWebhook(
            url_callback=url_callback,
            currency=currency,
            network=network,
            uuid=uuid,
            status=status,
            order_id=order_id
        )
        request_data = webhook_data.model_dump(exclude_none=False)
        result = await self._get_result_data(method="POST", endpoint=endpoint, data=request_data)
        return result

