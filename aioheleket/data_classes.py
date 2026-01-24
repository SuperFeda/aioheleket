from dataclasses import dataclass
from datetime import datetime
from typing import Union, Optional, Any, Dict, List

from .types.aliases import Currency
from .enums import (
    CryptoCurrency,
    Network,
    PaymentStatus,
    PayoutStatus
)


@dataclass
class Response:
    json: Union[Dict[str, Any], List[Dict[str, Any]]]
    status: int


@dataclass
class Wallet:
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
        network (Union[Network, str]): Network code identifying the blockchain network.
            Can be either a Network enum value or a string if the network is not predefined.
        currency (Union[CryptoCurrency, str]): Currency code of the wallet's network.
            Can be either a CryptoCurrency enum value or a string for custom currencies.
        url (str): URL of the payment form associated with this wallet.
    """
    wallet_uuid: str
    uuid: str
    address: str
    order_id: str
    network: Union[Network, str]
    currency: Union[CryptoCurrency, str]
    url: str


@dataclass
class PaymentConvert:
    """
    Information about automatic currency conversion for a payment.

    This structure is present when automatic conversion is enabled for the payer_currency
    (e.g., automatic conversion from BTC to USDT).

    Attributes:
        to_currency (str): The currency code that the payment will be converted to.
        commission (str): Conversion commission amount.
        rate (str): Conversion rate applied.
        amount (str): Converted amount in `to_currency` that was added to the merchant's balance,
            after deducting all commissions. This amount equals `merchant_amount * rate`.
    """
    to_currency: str
    commission: str
    rate: str
    amount: str
@dataclass
class Payment:
    """
    Represents an invoice/payment object in the payment system.

    Contains all information about a payment invoice including amounts, currencies,
    payment details, status, and timestamps.

    Notes:
        - All timestamps use UTC+3 timezone.
        - String amounts are used to maintain precision for cryptocurrency values.
        - The ``txid`` field may be absent in certain P2P payment scenarios.

    Attributes:
        uuid (str): Unique identifier of the invoice.
        order_id (str): Order identifier in the merchant's system.
        amount (str): Invoice amount.
        status (PaymentStatus): Payment status (from PaymentStatus enum).
        commission (str): Heleket commission amount.
        payment_amount (Optional[str]): Amount actually paid by the customer.
        payment_amount_usd (Optional[str]): Amount actually paid by the customer in USD.
        discount_percent (int): Percentage of discount or additional fee passed in request parameters.
        discount (str): Actual discount or additional fee amount in cryptocurrency.
            Example: If invoice amount is 15 USD and discount_percent is -5,
            discount value will be -0.75. Formula: amount + discount = payer_amount.
        payer_amount (str): Amount in ``payer_currency`` that the customer must pay,
            including discount or additional fee.
        payer_currency (CryptoCurrency): Currency in which the customer must make payment.
            If null, customer can choose specific currency on payment page.
        currency (CryptoCurrency): Invoice currency code.
        merchant_amount (str): Amount in cryptocurrency that will be credited to merchant's balance.
            If ``payer_currency`` parameter is not specified in invoice, value will be null.
        network (Network): Blockchain network code.
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
    amount: str
    status: PaymentStatus
    commission: str
    payment_amount: Optional[str]
    payment_amount_usd: Optional[str]
    discount_percent: int
    discount: str
    payer_amount: str
    payer_currency: CryptoCurrency
    payer_amount_exchange_rate: Optional[str]
    currency: CryptoCurrency
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
class PayoutConvert:
    """
    Represents conversion information for a payout.

    This structure contains details about the currency conversion that occurs during a payout.
    It is only present when the payout involves converting from one currency to another.

    Attributes:
        to_currency (str): The target currency code to which the payment is converted.
        from_currency (str): The source currency code from which the payment is converted.
        from_amount (str): The amount in ``from_currency`` that was deducted from the balance, after deducting all commissions.
        commission (str): The conversion commission amount.
        rate (str): The conversion rate applied.
    """
    to_currency: str
    from_currency: str
    from_amount: str
    commission: str
    rate: str
@dataclass
class Payout:
    """
    Represents a payout transaction in the payment system.

    This class contains all information about a payout including amounts, currencies,
    transaction details, status, and conversion information if applicable.

    Attributes:
        uuid (str): Unique identifier of the payout.
        amount (str): The payout amount in ``currency``.
        currency (CryptoCurrency): The currency code for the payout.
        commissions (str): The service commission amount.
        merchant_amount (str): The amount deducted from the merchant's balance, including all commissions.
        network (Network): The blockchain network code in which the payment is made.
        address (str): The wallet address to which the payment is made.
        txid (Optional[str]): The transaction identifier in the blockchain.
        status (PayoutStatus): The status of the payout (see all available statuses).
        is_final (bool): Whether the payout is finalized.
            The payout process is considered finalized once it has been successfully paid
            or if it has failed. In case of a failed payout, the funds will be returned
            to the merchant's balance, requiring a restart of the payout process.
        balance (str): The remaining funds on the merchant's balance.
        payer_currency (str): The cryptocurrency code in which the payout is actually made.
            The payout currency will be sent to the payout address.
        payer_amount (str): The payout amount in the payer's currency.
        convert (Optional[PayoutConvert]): Conversion information.
            Conversion is performed from ``from_currency`` to ``to_currency``.
            This field will not exist (None) if ``from_currency`` was not provided,
            or if it matches ``to_currency``.
    """
    uuid: str
    amount: str
    currency: CryptoCurrency
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
    """
    Attributes:
        commission (str):	Heleket commission amount
        merchant_amount (str): The amount to be removed from the merchant's balance
        payout_amount (str): The amount that was sent to the address.
    """
    commission: str
    merchant_amount: str
    payout_amount: str


@dataclass
class Transfer:
    """
    Represents a transfer transaction between a personal wallet and a business wallet.

    This class contains information about a transfer operation, including transaction identifiers
    and resulting balances for both personal and business wallets.

    Attributes:
        user_wallet_transaction_uuid (str): Unique identifier of the transaction
            in the personal wallet.
        user_wallet_balance (str): Balance of the personal wallet after the transfer.
        merchant_transaction_uuid (str): Unique identifier of the transaction
            in the business wallet.
        merchant_balance (str): Balance of the business wallet after the transfer.
    """
    user_wallet_transaction_uuid: str
    user_wallet_balance: str
    merchant_transaction_uuid: str
    merchant_balance: str


@dataclass
class ServiceLimit:
    """
    Represents the payment amount limits for a service.

    This class defines the minimum and maximum amounts that can be paid using a particular payment method or currency.

    Attributes:
        min_amount (str): The minimum amount available for payment.
        max_amount (str): The maximum amount available for payment.
    """
    min_amount: str
    max_amount: str
@dataclass
class ServiceCommission:
    """
    Represents the commission structure for a payment service.

    This class defines the fee structure applied to transactions, including
    both fixed and percentage-based fees.

    Attributes:
        fee_amount (str): Fixed commission amount.
        percent (str): Percentage commission fee for Heleket payment.
    """
    fee_amount: str
    percent: str
@dataclass
class Service:
    """
    This class contains comprehensive information about a payment method including
    blockchain network details, currency specifications, availability status,
    transaction limits, and commission fees.

    Attributes:
        network (Network): Blockchain network code.
        currency (CryptoCurrency): Currency code.
        is_available (bool): Indicates whether the payment method is available (true) or not (false).
        limit (ServiceLimit): Payment amount limits for this service.
        commission (ServiceCommission): Commission fees applied to transactions using this service.
    """
    network: Network
    currency: CryptoCurrency
    is_available: bool
    limit: ServiceLimit
    commission: ServiceCommission


@dataclass
class Discount:
    """
    Represents a discount configuration for a specific cryptocurrency and network.

    This class contains info of the discount percentage applicable to transactions
    using a particular cryptocurrency on a specific blockchain network.

    Attributes:
        currency (CryptoCurrency): Currency code to which the discount applies.
        network (Network): Blockchain network code to which the discount applies.
        discount (int): Discount percentage applied to transactions.
    """
    currency: CryptoCurrency
    network: Network
    discount: int


@dataclass
class Course:
    """
    Represents an exchange rate between two currencies.

    This class defines the conversion rate for exchanging one cryptocurrency
    to another currency (which could be a cryptocurrency or fiat currency).

    Attributes:
        from_ (CryptoCurrency): The source currency code from which the exchange is made.
        to (Currency): The target currency code to which the exchange is made.
        course (str): The exchange rate for converting from the source to target currency.
    """
    from_: CryptoCurrency
    to: Currency
    course: str


@dataclass
class CurrencyBalance:
    """
    The class that stores information about the amount of any currency in a balance.

    Attributes:
        currency_code (CryptoCurrency): code of cryptocurrency
        crypto_amount (str): amount in cryptocurrency
        usd_amount (str): amount in USD
        uuid (str): Wallet UUID
    """
    currency_code: CryptoCurrency
    crypto_amount: str
    usd_amount: str
    uuid: str
@dataclass
class Balance:
    """
    The class contains balance information for the merchant and the user.

    Attributes:
        merchant (List[CurrencyBalance]): Balance on the merchant.
        user (List[CurrencyBalance]): Balance on the user.
    """
    merchant: List[CurrencyBalance]
    user: List[CurrencyBalance]


@dataclass
class Pagination:
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
@dataclass
class PayoutDataInHistory:
    uuid: str
    amount: str
    currency: CryptoCurrency
    network: Network
    address: str
    txid: Optional[str]
    status: PayoutStatus
    is_final: bool
    balance: str
    created_at: datetime
    updated_at: datetime
@dataclass
class PaymentDataInHistory:
    uuid: str
    order_id: str
    amount: str
    payment_amount_usd: str
    payment_amount: Optional[str]
    payer_amount: str
    payer_amount_exchange_rate: Optional[str]
    discount_percent: Optional[int]
    discount: str
    payer_currency: str
    currency: str
    comments: Optional[str]
    merchant_amount: Optional[str]
    network: Optional[str]
    address: Optional[str]
    from_: Optional[str]
    txid: Optional[str]
    additional_data: Optional[str]
    commission: Optional[str]
    address_qr_code: Optional[str]
    payment_status: PaymentStatus
    status: PaymentStatus
    url: str
    expired_at: int
    is_final: bool
    created_at: datetime
    updated_at: datetime
@dataclass
class History:
    """
    Attributes:
        items (Union[List[PayoutDataInHistory], List[PaymentDataInHistory]]): List of operations. Can contain either
            payout data (PayoutDataInHistory) or payment data (PaymentDataInHistory).
        paginate (Pagination): Pagination object containing information about the number of
            elements on the current page and cursors to the previous and next pages.
    """
    items: Union[List[PayoutDataInHistory], List[PaymentDataInHistory]]
    paginate: Pagination


