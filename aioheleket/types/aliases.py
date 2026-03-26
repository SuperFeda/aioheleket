from typing import Union, Literal

from aioheleket.enums import (
    CryptoCurrency,
    FiatCurrency,
    Network,
    StaticWalletStatus,
    PayoutStatus,
    PaymentStatus,
    CourseSource,
    Priority
)

HttpMethod = Literal["POST", "GET"]
Currency = Union[FiatCurrency, CryptoCurrency, str]
CryptoCurrencyStr = Union[CryptoCurrency, str]
FiatCurrencyStr = Union[FiatCurrency, str]
NetworkStr = Union[Network, str]
PaymentStatusStr = Union[PaymentStatus, str]
PayoutStatusStr = Union[PayoutStatus, str]
StaticWalletStatusStr = Union[StaticWalletStatus, str]
CourseSourceStr = Union[CourseSource, str]
PriorityStr = Union[Priority, str]
