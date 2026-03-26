import hashlib
import base64
import json
import asyncio

from typing import Optional, Any, Dict
from aiohttp import ClientSession, ClientError

from .types.aliases import HttpMethod
from .data_classes import Response, RequestConfig
from .exceptions import (
    HeleketError,
    AioheleketError,
    InvalidCredentialsError,
    HeleketServerError,
    HeleketValidationError,
    NetworkError
)


class RequestBuilder:
    def __init__(self, session: ClientSession, merchant_id: str, api_key: str, config: Optional[RequestConfig] = None) -> None:
        self.__session = session
        self.__merchant_id = merchant_id
        self.__api_key = api_key
        self._config = config or RequestConfig()
        self._api_url = "https://api.heleket.com/v1/"

    @staticmethod
    def _format_json(data: Optional[Dict[str, Any]]) -> str:
        return json.dumps(data, separators=(",", ":"))

    def _gen_sign(self, data: Optional[str] = None) -> str:
        encoded_data = base64.b64encode(data.encode("utf-8") if data else b"")
        encoded_api_key = self.__api_key.encode("utf-8")
        return hashlib.md5(encoded_data + encoded_api_key).hexdigest()

    def _gen_headers(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "merchant": self.__merchant_id,
            "sign": (
                self._gen_sign(self._format_json(data))
                if data
                else self._gen_sign()
            )
        }

    def _get_url(self, endpoint: str) -> str:
        return self._api_url.rstrip("/") + "/" + endpoint.lstrip("/")

    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        return await self._create_request(method="POST", url=self._get_url(endpoint), data=data, **kwargs)

    async def get(self, endpoint: str, **kwargs) -> Response:
        return await self._create_request(method="GET", url=self._get_url(endpoint), **kwargs)

    async def _create_request(self, method: HttpMethod, url: str, data: Optional[Dict[str, Any]] = None, **kwargs):
        for attempt in range(self._config.max_retries+1):
            try:
                async with self.__session.request(
                        method=method,
                        url=url,
                        data=self._format_json(data) if data else None,
                        headers=self._gen_headers(data),
                        **kwargs
                ) as response:
                    response_data = (await response.json())
                    response_status = response.status
                    if not response_data:
                        await self.__session.close()
                        raise AioheleketError(message="Empty JSON response", method=url, status_code=response_status)

                    state = response_data.get("state")

                    if response_status == 401 and response_data.get("message") == "Invalid Sign.":
                        await self.__session.close()
                        raise InvalidCredentialsError(
                            message="Invalid payment_api_key/payout_api_key or merchant_id in HeleketClient",
                            status_code=response_status,
                            method=url,
                        )

                    if response_status == 500:
                        await self.__session.close()
                        raise HeleketServerError(
                            message=f"Heleket server error. {response_data.get('message')}. Error: {response_data.get('error')}",
                            method=url,
                            status_code=response_status
                        )

                    if response_status != 200 or (state is not None and state != 0):
                        await self.__session.close()
                        if "errors" in response_data:
                            raise HeleketValidationError(
                                message="Validation error",
                                status_code=response_status,
                                method=url,
                                errors=response_data.get("errors"),
                            )
                        raise AioheleketError(
                            message=response_data.get("message", "API error"),
                            status_code=response_status,
                            method=url,
                            json_response=response_data,
                        )

                    if response_data.get("result", None) is None:
                        await self.__session.close()
                        raise HeleketError(f"Failed to get result. (Status code: {response_status}; Method: {url}; Response: {response_data})")

                    return Response(json=response_data, status=response_status)

            except (ClientError, asyncio.TimeoutError) as e:
                if attempt < self._config.max_retries:
                    await asyncio.sleep(self._config.retry_backoff_s * (2 ** attempt))
                    continue
                raise NetworkError("Network error", e)

