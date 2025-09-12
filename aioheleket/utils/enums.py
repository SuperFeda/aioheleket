from enum import StrEnum, IntEnum


class Currency(StrEnum):
    """
    doc https://doc.heleket.com/ru/other/reference
    """
    VERSE = "VERSE"
    HMSTR = "HMSTR"
    CGPT = "CGPT"
    AVAX = "AVAX"
    DASH = "DASH"
    DOGE = "DOGE"
    SHIB = "SHIB"
    USDC = "USDC"
    USDT = "USDT"
    BCH = "BCH"
    BNB = "BNB"
    BTC = "BTC"
    DAI = "DAI"
    ETH = "ETH"
    LTC = "LTC"
    POL = "POL"
    SOL = "SOL"
    TON = "TON"
    TRX = "TRX"
    XMR = "XMR"


class Network(StrEnum):
    """
    doc https://doc.heleket.com/ru/other/reference
    """
    AVALANCHE = "AVALANCHE"
    ARBITRUM = "ARBITRUM"
    POLYGON = "POLYGON"
    TRON = "TRON"
    DASH = "DASH"
    DOGE = "DOGE"
    ETH = "ETH"
    BCH = "BCH"
    BSC = "BSC"
    BTC = "BTC"
    LTC = "LTC"
    SOL = "SOL"
    TON = "TON"
    XMR = "XMR"


class CourseSource(StrEnum):
    """
    Enum of services from which the exchange
    rates for invoice recalculation are taken
    """
    BINANCE = "Binance"
    BINANCEP2P = "BinanceP2P"
    EXMO = "Exmo"
    KUCOIN = "Kucoin"
    GARANTEXIO = "Garantexio"


class PaymentStatus(StrEnum):
    """
    doc https://doc.heleket.com/ru/methods/payments/payment-statuses
    """
    PROCESS = "process"
    CHECK = "check"
    PAID = "paid"
    PAID_OVER = "paid_over"
    FAIL = "fail"
    WRONG_AMOUNT = "wrong_amount"
    CANCEL = "cancel"
    SYSTEM_FAIL = "system_fail"
    REFUND_PROCESS = "refund_process"
    REFUND_FAIL = "refund_fail"
    REFUND_PAID = "refund_paid"
    LOCKED = "locked"


class PayoutStatus(StrEnum):
    SYSTEM_FAIL = "system_fail"
    PROCESS = "process"
    CANCEL = "cancel"
    CHECK = "check"
    PAID = "paid"
    FAIL = "fail"


class StaticWalletStatus(StrEnum):
    BLOCKED = "blocked"
    ACTIVE = "active"
    IN_ACTIVE = "in_active"


class Priority(StrEnum):
    RECOMMENDED = "recommended"
    ECONOMY = "economy"
    HIGH = "high"
    HIGHEST = "highest"


class Lifetime(IntEnum):
    """
    Payment Time To Live in seconds
    """
    MINUTE_5 = 300  # min value for lifetime
    MINUTE_10 = 600
    MINUTE_15 = 900
    MINUTE_20 = 1200
    MINUTE_25 = 1500
    MINUTE_30 = 1800
    MINUTE_35 = 2100
    MINUTE_40 = 2400
    MINUTE_45 = 2700
    MINUTE_50 = 3000
    MINUTE_55 = 3300
    HOUR_1 = 3600  # default value for lifetime
    HOUR_2 = 7200
    HOUR_3 = 10800
    HOUR_4 = 14400
    HOUR_5 = 18000
    HOUR_6 = 21600
    HOUR_7 = 25200
    HOUR_8 = 28800
    HOUR_9 = 32400
    HOUR_10 = 36000
    HOUR_11 = 39600
    HOUR_12 = 43200  # max value for lifetime
