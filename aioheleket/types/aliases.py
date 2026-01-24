from typing import Union

from ..enums import CryptoCurrency, FiatCurrency

Currency = Union[FiatCurrency, CryptoCurrency, str]
