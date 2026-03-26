from __future__ import annotations

from typing import List, Optional, Union
from datetime import datetime
from decimal import Decimal
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    EmailStr,
    UUID4
)

from aioheleket.enums import (
    Priority,
    PaymentStatus,
    StaticWalletStatus,
    PayoutStatus
)
from aioheleket.types.aliases import (
    Currency,
    CourseSourceStr,
    CryptoCurrencyStr,
    FiatCurrencyStr,
    NetworkStr,
    PriorityStr
)
from .fields import OrderID128, OrderID100


class _BaseScheme(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        use_enum_values=True,
    )


class CreatePayment(_BaseScheme):
    amount: str
    currency: CryptoCurrencyStr
    order_id: OrderID128
    network: Optional[NetworkStr] = None
    url_return: Optional[HttpUrl] = Field(None, min_length=6, max_length=255)
    url_success: Optional[HttpUrl] = Field(None, min_length=6, max_length=255)
    url_callback: Optional[HttpUrl] = Field(None, min_length=6, max_length=255)
    is_payment_multiple: bool = True
    lifetime: int = Field(3600, ge=300, le=43200)
    to_currency: Optional[CryptoCurrencyStr] = None
    subtract: int = Field(0, ge=0, le=100)
    accuracy_payment_percent: int = Field(0, ge=0, le=5)
    additional_data: Optional[str] = Field(None, max_length=255)
    currencies: Optional[List[ShortCurrencyInfo]] = None
    except_currencies: Optional[List[ShortCurrencyInfo]] = None
    course_source: Optional[CourseSourceStr] = None
    from_referral_code: Optional[str] = None
    discount_percent: Optional[int] = Field(None, ge=-99, le=100)
    is_refresh: bool = False
    payer_email: Optional[EmailStr] = None


class CreatePayout(_BaseScheme):
    amount: str
    currency: Currency
    address: str
    is_subtract: bool
    order_id: OrderID100
    network: Optional[NetworkStr] = None
    url_callback: Optional[HttpUrl] = Field(None, min_length=6, max_length=255)
    to_currency: Optional[CryptoCurrencyStr] = None
    course_source: Optional[CourseSourceStr] = None
    from_currency: Optional[str] = None
    priority: PriorityStr = Field(Priority.RECOMMENDED, validate_default=True)
    memo: Optional[str] = Field(None, min_length=1, max_length=30)


class CreateWallet(_BaseScheme):
    currency: CryptoCurrencyStr
    network: NetworkStr
    order_id: OrderID100
    url_callback: Optional[HttpUrl] = Field(None, min_length=6, max_length=255)
    from_referral_code: Optional[str] = None


class TestWebhook(_BaseScheme):
    url_callback: HttpUrl = Field(min_length=6, max_length=150)
    currency: CryptoCurrencyStr
    network: NetworkStr
    status: Union[str, PaymentStatus, PayoutStatus, StaticWalletStatus] = Field(PaymentStatus.PAID, validate_default=True)
    order_id: Optional[str] = Field(None, min_length=1, max_length=32, pattern=r"^[a-zA-Z0-9_-]+$")
    uuid: Optional[UUID4] = None


class ShortCurrencyInfo(_BaseScheme):
    currency: CryptoCurrencyStr
    network: Optional[NetworkStr] = None


class Payment(_BaseScheme):
    """
    Represents an invoice/payment object in the payment system.

    Contains all information about a payment invoice including amounts, currencies,
    payment details, status, and timestamps.

    Notes:
        - All timestamps use UTC+3 timezone.
        - The ``txid`` field may be absent in certain P2P payment scenarios.

    Attributes:
        uuid (str): Unique identifier of the invoice.
        order_id (str): Order identifier in the merchant's system.
        amount (Decimal): Invoice amount.
        status (str): Payment status.
        commission (str): Heleket commission amount.
        payment_amount (Optional[Decimal]): Amount actually paid by the customer.
        payment_amount_usd (Optional[Decimal]): Amount actually paid by the customer in USD.
        discount_percent (Decimal): Percentage of discount or additional fee passed in request parameters.
        discount (Decimal): Actual discount or additional fee amount in cryptocurrency.
            Example: If invoice amount is 15 USD and discount_percent is -5,
            discount value will be -0.75. Formula: amount + discount = payer_amount.
        payer_amount (Decimal): Amount in ``payer_currency`` that the customer must pay,
            including discount or additional fee.
        payer_currency (str): Currency in which the customer must make payment.
            If null, customer can choose specific currency on payment page.
        currency (str): Invoice currency code.
        merchant_amount (Optional[Decimal]): Amount in cryptocurrency that will be credited to merchant's balance.
            If ``payer_currency`` parameter is not specified in invoice, value will be null.
        network (str): Blockchain network code.
        address (str): Wallet address for payment.
        from_ (Optional[str]): Wallet address from which payment was made.
        txid (Optional[str]): Transaction hash in blockchain.
            This field won't exist if:
            1) Payment was made via P2P (customer withdrew from their Heleket account to the invoice address)
            2) Payment hasn't been made
            3) Payment had issues or customer made an error and it was marked as "paid" manually
        payment_status (str): Payment status (string representation).
        url (str): URL of the payment page.
        expired_at (int): Invoice expiration timestamp.
        is_final (bool): Whether the invoice is finalized.
            When invoice is finalized, it cannot be paid (either paid or expired).
        additional_data (Optional[str]): Additional information.
        created_at (datetime): Invoice creation date (UTC+3 timezone).
        updated_at (datetime): Last invoice update date (UTC+3 timezone).
        comments (Optional[str]): Comments or notes.
        address_qr_code (str): QR code with wallet address for payment.
        convert (Optional[PaymentConvert]): Information about automatic currency conversion.
            Present only when automatic conversion is enabled for the payer_currency.
            If not enabled, this field will be None.
    """
    uuid: str
    order_id: str
    amount: Decimal
    status: str
    commission: Optional[Decimal]
    payment_amount: Optional[Decimal]
    payment_amount_usd: Optional[Decimal]
    discount_percent: Optional[Decimal]
    discount: Decimal
    payer_amount: Decimal
    payer_currency: str
    payer_amount_exchange_rate: Optional[str]
    currency: str
    merchant_amount: Optional[Decimal]
    network: Optional[str]
    address: Optional[str]
    from_: Optional[str] = Field(..., alias="from")
    txid: Optional[str]
    payment_status: str
    url: str
    expired_at: int
    is_final: bool
    additional_data: Optional[str]
    created_at: datetime
    updated_at: datetime
    comments: Optional[str]
    address_qr_code: Optional[str]
    convert: Optional[PaymentConvert] = None
class PaymentConvert(_BaseScheme):
    """
    Information about automatic currency conversion for a payment.

    This structure is present when automatic conversion is enabled for the ``payer_currency``
    (e.g., automatic conversion from BTC to USDT).

    Attributes:
        to_currency (str): The currency code that the payment will be converted to.
        commission (Decimal): Conversion commission amount.
        rate (str): Conversion rate applied.
        amount (Decimal): Converted amount in `to_currency` that was added to the merchant's balance,
            after deducting all commissions. This amount equals `merchant_amount * rate`.
    """
    to_currency: str
    commission: Decimal
    rate: str
    amount: Decimal

class CreatePaymentRefund(_BaseScheme):
    """
    Attributes:
        address (str): The address to which the refund should be made
        is_subtract (bool): Whether to take a commission from the merchant's balance or from the refund amount:
            true - take the commission from merchant balance.
            false - reduce the refundable amount by the commission amount.
        uuid (str): Invoice uuid
        order_id (str): Invoice order ID
        amount (str): Refund amount
    """
    address: str
    is_subtract: bool
    uuid: UUID4
    order_id: OrderID128
    amount: Optional[str] = Field(None, max_length=40)

class StaticWallet(_BaseScheme):
    """
    Represents a merchant's wallet for a specific blockchain network.

    This class contains information about a wallet address used for receiving payments
    in a particular cryptocurrency and network. It includes both the merchant's
    master wallet identifier and the specific network wallet details.

    Attributes:
        wallet_uuid (str): Unique identifier of the merchant's master wallet.
        uuid (str): Unique identifier of the wallet in the specific network.
        address (str): Blockchain wallet address for the specified network.
        order_id (str): Order identifier in the merchant's system (for order tracking).
        network (str): Network code identifying the blockchain network.
            Can be either a Network enum value or a string if the network is not predefined.
        currency (str): Currency code of the wallet's network.
            Can be either a CryptoCurrency enum value or a string for custom currencies.
        url (str): URL of the payment form associated with this wallet.
    """
    wallet_uuid: str
    uuid: str
    address: str
    order_id: str
    network: str
    currency: str
    url: str

class Payout(_BaseScheme):
    """
    Represents a payout transaction in the payment system.

    This class contains all information about a payout including amounts, currencies,
    transaction details, status, and conversion information if applicable.

    Attributes:
        uuid (str): Unique identifier of the payout.
        amount (Decimal): The payout amount in ``currency``.
        currency (str): The currency code for the payout.
        commissions (str): The service commission amount.
        merchant_amount (str): The amount deducted from the merchant's balance, including all commissions.
        network (Network): The blockchain network code in which the payment is made.
        address (str): The wallet address to which the payment is made.
        txid (Optional[str]): The transaction identifier in the blockchain.
        status (str): The status of the payout (see all available statuses).
        is_final (bool): Whether the payout is finalized.
            The payout process is considered finalized once it has been successfully paid
            or if it has failed. In case of a failed payout, the funds will be returned
            to the merchant's balance, requiring a restart of the payout process.
        balance (Decimal): The remaining funds on the merchant's balance.
        payer_currency (str): The cryptocurrency code in which the payout is actually made.
            The payout currency will be sent to the payout address.
        payer_amount (Decimal): The payout amount in the payer's currency.
        convert (Optional[PayoutConvert]): Conversion information.
            Conversion is performed from ``from_currency`` to ``to_currency``.
            This field will not exist (None) if ``from_currency`` was not provided,
            or if it matches ``to_currency``.
    """
    uuid: str
    amount: Decimal
    currency: str
    commissions: Decimal
    merchant_amount: Decimal
    network: str
    address: str
    txid: Optional[str]
    status: str
    is_final: bool
    balance: Decimal
    payer_currency: str
    payer_amount: Decimal
    convert: Optional[PayoutConvert] = None
class PayoutConvert(_BaseScheme):
    """
    Represents conversion information for a payout.

    This structure contains details about the currency conversion that occurs during a payout.
    It is only present when the payout involves converting from one currency to another.

    Attributes:
        to_currency (str): The target currency code to which the payment is converted.
        from_currency (str): The source currency code from which the payment is converted.
        from_amount (Decimal): The amount in ``from_currency`` that was deducted from the balance, after deducting all commissions.
        commission (Decimal): The conversion commission amount.
        rate (str): The conversion rate applied.
    """
    to_currency: str
    from_currency: str
    from_amount: Decimal
    commission: Decimal
    rate: str

class CreatePayoutWithdrawalAmount(_BaseScheme):
    amount: str
    address: str
    currency: FiatCurrencyStr
    to_currency: Optional[CryptoCurrencyStr] = None
    network: Optional[NetworkStr]
    is_subtract: bool
    course_source: CourseSourceStr = None
    priority: PriorityStr = Field(Priority.RECOMMENDED, validate_default=True)

class PayoutWithdrawalAmount(_BaseScheme):
    """
    Attributes:
        commission (Decimal): Heleket commission amount
        merchant_amount (Decimal): The amount to be removed from the merchant's balance
        payout_amount (Decimal): The amount that was sent to the address.
    """
    commission: Decimal
    merchant_amount: Decimal
    payout_amount: Decimal

class Transfer(_BaseScheme):
    """
    Represents a transfer transaction between a personal wallet and a business wallet.

    This class contains information about a transfer operation, including transaction identifiers
    and resulting balances for both personal and business wallets.

    Attributes:
        user_wallet_transaction_uuid (str): Unique identifier of the transaction in the personal wallet.
        user_wallet_balance (Decimal): Balance of the personal wallet after the transfer.
        merchant_transaction_uuid (str): Unique identifier of the transaction in the business wallet.
        merchant_balance (Decimal): Balance of the business wallet after the transfer.
    """
    user_wallet_transaction_uuid: str
    user_wallet_balance: Decimal
    merchant_transaction_uuid: str
    merchant_balance: Decimal

class Discount(_BaseScheme):
    """
    Represents a discount configuration for a specific cryptocurrency and network.

    This class contains info of the discount percentage applicable to transactions
    using a particular cryptocurrency on a specific blockchain network.

    Attributes:
        currency (CryptoCurrencyStr): Currency code to which the discount applies.
        network (NetworkStr): Blockchain network code to which the discount applies.
        discount (int): Discount percentage applied to transactions.
    """
    currency: CryptoCurrencyStr
    network: NetworkStr
    discount: int = Field(0, ge=-99, le=100)

class ServiceLimit(_BaseScheme):
    """
    Represents the payment amount limits for a service.

    This class defines the minimum and maximum amounts that can be paid using a particular payment method or currency.

    Attributes:
        min_amount (Decimal): The minimum amount available for payment.
        max_amount (Decimal): The maximum amount available for payment.
    """
    min_amount: Decimal
    max_amount: Decimal
class ServiceCommission(_BaseScheme):
    """
    Represents the commission structure for a payment service.

    This class defines the fee structure applied to transactions, including
    both fixed and percentage-based fees.

    Attributes:
        fee_amount (Decimal): Fixed commission amount.
        percent (Decimal): Percentage commission fee for Heleket payment.
    """
    fee_amount: Decimal
    percent: Decimal
class Service(_BaseScheme):
    """
    This class contains comprehensive information about a payment method including
    blockchain network details, currency specifications, availability status,
    transaction limits, and commission fees.

    Attributes:
        network (str): Blockchain network code.
        currency (str): Currency code.
        is_available (bool): Indicates whether the payment method is available (true) or not (false).
        limit (ServiceLimit): Payment amount limits for this service.
        commission (ServiceCommission): Commission fees applied to transactions using this service.
    """
    network: str
    currency: str
    is_available: bool
    limit: ServiceLimit
    commission: ServiceCommission

class Course(_BaseScheme):
    """
    Represents an exchange rate between two currencies.

    This class defines the conversion rate for exchanging one cryptocurrency
    to another currency (which could be a cryptocurrency or fiat currency).

    Attributes:
        from_ (str): The source currency code from which the exchange is made.
        to (str): The target currency code to which the exchange is made.
        course (Decimal): The exchange rate for converting from the source to target currency.
    """
    from_: str = Field(..., alias="from")
    to: str
    course: Decimal

class CurrencyBalance(_BaseScheme):
    """
    The class that stores information about the amount of any currency in a balance.

    Attributes:
        currency_code (str): code of cryptocurrency
        crypto_balance (Decimal): amount in cryptocurrency
        usd_balance (Decimal): amount in USD
        uuid (str): Wallet UUID
    """
    currency_code: str
    crypto_balance: Decimal = Field(..., alias="balance")
    usd_balance: Decimal = Field(..., alias="balance_usd")
    uuid: str
class Balance(_BaseScheme):
    """
    The class contains balance information for the merchant and the user.

    Attributes:
        merchant (List[CurrencyBalance]): Balance on the merchant.
        user (List[CurrencyBalance]): Balance on the user.
    """
    merchant: List[CurrencyBalance]
    user: List[CurrencyBalance]

class Pagination(_BaseScheme):
    """
    This class contains information about the current page, navigation cursors, and pagination limits.

    Attributes:
        count (int): Number of items on the current page.
        hasPages (bool): Whether there are enough items to split into multiple pages.
        nextCursor (Optional[str]): Cursor for retrieving the next page. ``None`` if this is the last page.
        previousCursor (Optional[str]): Cursor for retrieving the previous page. ``None`` if this is the first page.
        perPage (int): Maximum number of items that can be returned per page.
    """
    count: int
    hasPages: bool
    nextCursor: Optional[str]
    previousCursor: Optional[str]
    perPage: int
class PayoutDataInHistory(_BaseScheme):
    uuid: str
    amount: Decimal
    currency: str
    network: str
    address: str
    txid: Optional[str]
    status: str
    is_final: bool
    balance: Decimal
    created_at: datetime
    updated_at: datetime
class PaymentDataInHistory(_BaseScheme):
    uuid: str
    order_id: str
    amount: Decimal
    payment_amount_usd: Decimal
    payment_amount: Optional[Decimal]
    payer_amount: Decimal
    payer_amount_exchange_rate: Optional[Decimal]
    discount_percent: Optional[Decimal]
    discount: Decimal
    payer_currency: str
    currency: str
    comments: Optional[str]
    merchant_amount: Optional[Decimal]
    network: Optional[str]
    address: Optional[str]
    from_: Optional[str] = Field(..., alias="from")
    txid: Optional[str]
    additional_data: Optional[str]
    commission: Optional[Decimal]
    address_qr_code: Optional[str]
    payment_status: str
    status: str
    url: str
    expired_at: int
    is_final: bool
    created_at: datetime
    updated_at: datetime
class History(_BaseScheme):
    """
    Attributes:
        items (Union[List[PayoutDataInHistory], List[PaymentDataInHistory]]): List of operations. Can contain either
            payout data (PayoutDataInHistory) or payment data (PaymentDataInHistory).
        paginate (Pagination): Pagination object containing information about the number of
            elements on the current page and cursors to the previous and next pages.
    """
    items: Union[List[PayoutDataInHistory], List[PaymentDataInHistory]]
    paginate: Pagination