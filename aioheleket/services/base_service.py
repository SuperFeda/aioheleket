from datetime import datetime
from typing import Dict, Any, Optional, Union, Literal, List

from ..data_classes import (
    Response,
    Service,
    ServiceLimit,
    ServiceCommission
)
from ..enums import (
    PaymentStatus,
    PayoutStatus,
    StaticWalletStatus,
    Network,
    CryptoCurrency
)
from ..utils.request_builder import RequestBuilder
from ..utils.schemas import TestWebhookScheme


class _BaseService:
    def __init__(self, request_builder: RequestBuilder):
        self._request_builder = request_builder
        self.__api_url = "https://api.heleket.com/v1"

    async def _get_response(self,
                            method: Literal["POST", "GET"],
                            endpoint: str,
                            data: Optional[Dict[str, Any]] = None
                            ) -> Response:
        if method not in ("POST", "GET"):
            raise ValueError("The method must be either POST or GET")

        if method == "POST":
            return await self._request_builder.post(url=self.__api_url + endpoint, data=data)
        elif method == "GET":
            return await self._request_builder.get(url=self.__api_url + endpoint)

    async def _get_result_data(self,
                               method: Literal["POST", "GET"],
                               endpoint: str,
                               data: Optional[Dict[str, Any]] = None
                               ) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        response = await self._get_response(method=method, endpoint=endpoint, data=data)
        data = response.json
        result = data.get("result", None)
        return result

    async def _get_qr_image_base64(self, endpoint: str, request_data: Dict[str, str]) -> str:
        result = await self._get_result_data("POST", endpoint, request_data)
        base64_qr_image = result.get("image")
        return base64_qr_image

    async def _get_services_info(self, endpoint: str) -> List[Service]:
        result = await self._get_result_data("POST", endpoint)
        services_list = []
        for service in result:
            service_limit = ServiceLimit(**service.pop("limit"))
            service_commission = ServiceCommission(**service.pop("commission"))
            services_list.append(Service(**service, limit=service_limit, commission=service_commission))
        return services_list

    async def _get_history_data(self,
                                endpoint: str,
                                date_from: Optional[Union[str, datetime]] = None,
                                date_to: Optional[Union[str, datetime]] = None
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
                                   currency: Union[CryptoCurrency, str],
                                   network: Union[Network, str],
                                   status: Union[PaymentStatus, PayoutStatus, StaticWalletStatus],
                                   uuid: Optional[str] = None,
                                   order_id: Optional[str] = None,
                                   ) -> List:
        request_data = {
            "url_callback": url_callback,
            "currency": currency,
            "network": network,
            "uuid": uuid,
            "status": status,
            "order_id": order_id
        }
        TestWebhookScheme.model_validate(request_data)
        result = await self._get_result_data(method="POST", endpoint=endpoint, data=request_data)
        return result

