from dataclasses import dataclass
from typing import Union, Any, Dict, List


@dataclass(frozen=True)
class RequestConfig:
    """
    Attributes:
        timeout_s (float): total request timeout
        max_retries (int): retry count for network errors
        retry_backoff_s (float): base backoff delay (exponential)
        connector_limit (int): total TCPConnector connections
        connector_limit_per_host (int): per-host connection limit
        ttl_dns_cache (int): controls the Time-To-Live of DNS cache entries when making HTTP requests
    """
    timeout_s: float = 20.0
    max_retries: int = 2
    retry_backoff_s: float = 0.25
    connector_limit: int = 100
    connector_limit_per_host: int = 50
    ttl_dns_cache: int = 300


@dataclass(frozen=True)
class Response:
    json: Union[Dict[str, Any], List[Dict[str, Any]]]
    status: int




