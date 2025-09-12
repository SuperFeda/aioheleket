from pydantic import (
    BaseModel,
    ConfigDict,
    Field, HttpUrl
)
from typing import List, Optional, Union

from ..utils.enums import (
    Currency,
    Network,
    CourseSource,
    Priority,
    Lifetime, PaymentStatus
)


class OrderIDScheme(BaseModel):
    order_id: str = Field(min_length=1, max_length=128, pattern=r"^[a-zA-Z0-9_-]+$")


class PaymentScheme(OrderIDScheme):
    model_config = ConfigDict(from_attributes=True)

    # --- required
    amount: str
    currency: Union[str, Currency]

    # --- Optional
    network: Optional[Union[str, Network]] = None
    url_return: Optional[str] = Field(None, min_length=6, max_length=255)
    url_success: Optional[str] = Field(None, min_length=6, max_length=255)
    url_callback: Optional[str] = Field(None, min_length=6, max_length=255)
    is_payment_multiple: bool = True
    lifetime: int = Field(Lifetime.HOUR_1, ge=300, le=43200)
    to_currency: Optional[str] = None
    subtract: int = Field(0, ge=0, le=100)
    accuracy_payment_percent: float = Field(0.0, ge=0, le=5)
    additional_data: Optional[str] = Field(None, max_length=255)
    currencies: Optional[List[str]] = Field(default_factory=list)
    except_currencies: Optional[List[str]] = None
    course_source: Optional[CourseSource] = None
    from_referral_code: Optional[str] = None
    discount_percent: Optional[int] = Field(None, ge=-99, le=100)
    is_refresh: bool = False


class PaymentTestWebhook(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # --- required
    url_callback: HttpUrl = Field(min_length=6, max_length=150)
    currency: Union[str, Currency]
    network: Union[str, Network]
    status: PaymentStatus = PaymentStatus.PAID

    # --- Optional
    order_id: Optional[str] = Field(None, min_length=1, max_length=32, pattern=r"^[a-zA-Z0-9_-]+$")
    uuid: Optional[str] = None


class PayoutScheme(OrderIDScheme):
    model_config = ConfigDict(from_attributes=True)

    # --- required
    amount: str
    currency: Union[str, Currency]
    network: Union[str, Network]
    address: str
    is_subtract: bool

    # --- Optional
    url_callback: Optional[str] = None
    to_currency: Optional[str] = None
    course_source: Optional[CourseSource] = None
    from_currency: Optional[str] = None
    priority: Priority = Priority.RECOMMENDED
    memo: Optional[str] = Field(None, min_length=1, max_length=30)


class WalletScheme(OrderIDScheme):
    model_config = ConfigDict(from_attributes=True)

    # --- required
    currency: Union[str, Currency]
    network: Union[str, Network]

    # --- Optional
    url_callback: Optional[str] = Field(None, min_length=6, max_length=255)
    from_referral_code: Optional[str] = None

