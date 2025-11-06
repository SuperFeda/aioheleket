from dataclasses import dataclass
from datetime import datetime
from typing import Union, Optional, Any, Dict

from .enums import (
    Currency,
    Network,
    PaymentStatus,
    PayoutStatus
)


@dataclass
class Response:
    json: Dict[str, Any]
    status: int
    cookies: Dict


@dataclass
class PaymentConvert:
    to_currency: str
    commission: str
    rate: str
    amount: str


@dataclass
class PayoutConvert:
    to_currency: str
    from_currency: str
    from_amount: str
    commission: str
    rate: str


@dataclass
class Wallet:
    wallet_uuid: str
    uuid: str
    address: str
    order_id: str
    network: Union[Network, str]
    currency: Union[Currency, str]
    url: str


@dataclass
class Payment:
    uuid: str
    order_id: str
    amount: str
    status: PaymentStatus
    commission: str
    payment_amount: Optional[str]
    payment_amount_usd: Optional[str]
    discount_percent: int
    discount: str
    payer_amount: str
    payer_currency: Currency
    payer_amount_exchange_rate: Optional[str]
    currency: Currency
    merchant_amount: str
    network: Network
    address: str
    from_: Optional[str]
    txid: Optional[str]
    payment_status: str
    url: str
    expired_at: int
    is_final: bool
    additional_data: Optional[str]
    created_at: datetime
    updated_at: datetime
    comments: Optional[str]
    address_qr_code: str
    convert: Optional[PaymentConvert] = None


@dataclass
class Payout:
    uuid: str
    amount: str
    currency: Currency
    commissions: str
    merchant_amount: str
    network: Network
    address: str
    txid: Optional[str]
    status: PayoutStatus
    is_final: bool
    balance: str
    payer_currency: str
    payer_amount: str
    convert: Optional[PayoutConvert] = None


@dataclass
class PayoutSum:
    commission: str
    merchant_amount: str
    payout_amount: str


@dataclass
class Transfer:
    user_wallet_transaction_uuid: str
    user_wallet_balance: str
    merchant_transaction_uuid: str
    merchant_balance: str


@dataclass
class ServiceLimit:
    min_amount: str
    max_amount: str


@dataclass
class ServiceCommission:
    fee_amount: str
    percent: str


@dataclass
class Service:
    network: Network
    currency: Currency
    is_available: bool
    limit: ServiceLimit
    commission: ServiceCommission


@dataclass
class Discount:
    currency: Currency
    network: Network
    discount: int


@dataclass
class Course:
    from_: Currency
    to: str
    course: str


@dataclass
class Balance:
    currency_code: Currency
    balance: str
    balance_usd: str
    uuid: str
