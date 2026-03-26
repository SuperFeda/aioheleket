from typing import Dict, Any, Optional


class HeleketError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class AioheleketError(HeleketError):
    def __init__(self, message: str, method: str, status_code: int, json_response: Dict[str, Any] = None):
        msg = f"{message} (Status code: {status_code}; Method: {method}"
        if json_response is not None:
            msg += f"; Response: {json_response}"
        super().__init__(f"{msg})")


class InvalidCredentialsError(HeleketError):
    def __init__(self, message: str, method: str, status_code: int):
        super().__init__(f"{message} (Status code: {status_code}; Method: {method})")


class HeleketServerError(HeleketError):
    def __init__(self, message: str, method: str, status_code: int):
        super().__init__(f"{message} (Status code: {status_code}; Method: {method})")


class HeleketValidationError(HeleketError):
    def __init__(self, message: str, method: str, status_code: int, errors):
        super().__init__(f"{message} (Status code: {status_code}; Method: {method}; Errors: {errors})")


class NetworkError(HeleketError):
    def __init__(self, message: str, exc: Optional[Exception] = None):
        super().__init__(message if exc is None else f"{message}: {exc!r}")

