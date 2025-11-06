import hashlib
import base64
import json

from typing import Optional, Any, Union, Dict
from aiohttp import ClientSession

from .exceptions import HeleketError, HeleketValidationError, HeleketServerError
from ..utils.data_classes import Response


class RequestBuilder:
    def __init__(self, session: ClientSession, merchant_id: str, api_key: str) -> None:
        self.__session = session
        self.__merchant_id = merchant_id
        self.__api_key = api_key

    @staticmethod
    def __format_json(data: Optional[Dict[str, Any]]) -> Union[None, str]:
        return json.dumps(data, separators=(",", ":")) if data else None

    def __gen_sign(self, data: Optional[str] = None) -> str:
        data_to_sign = base64.b64encode(data.encode("utf-8") if data else b"")
        return hashlib.md5(data_to_sign + self.__api_key.encode("utf-8")).hexdigest()

    def __gen_headers(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "merchant": self.__merchant_id,
            "sign": (
                self.__gen_sign(self.__format_json(data))
                if data
                else self.__gen_sign()
            )
        }

    async def post(self, url: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        async with self.__session.post(url=url, data=self.__format_json(data), headers=self.__gen_headers(data), **kwargs) as response:

            res_data = (await response.json())

            if res_data.get("state") == 1:
                if res_data.get("message") is not None:
                    raise HeleketError(res_data.get("message"))
                if res_data.get("errors") is not None:
                    raise HeleketValidationError(f"The parameters were not passed: {res_data.get('errors')}")
                raise HeleketError("state: 1")

            if response.status == 500:
                raise HeleketServerError(f"{res_data.get('message')}. Error: {res_data.get('error')}")

            return Response(json=res_data, status=response.status, cookies=response.cookies)

    async def get(self, url: str, **kwargs) -> Response:
        async with self.__session.get(url=url, headers=self.__gen_headers(), **kwargs) as response:

            res_data = (await response.json())

            if res_data.get("state") == 1:
                if res_data.get("message") is not None:
                    raise HeleketError(res_data.get("message"))
                if res_data.get("errors") is not None:
                    raise HeleketValidationError(f"The parameters were not passed: {res_data.get('errors')}")
                raise HeleketError("state: 1")

            if response.status == 500:
                raise HeleketServerError(f"{res_data.get('message')}. Error: {res_data.get('error')}")

            return Response(json=res_data, status=response.status, cookies=response.cookies)
