# aioheleket

Asynchronous Python library for the [Heleket](https://heleket.com) crypto payment API.

[Usage examples](https://github.com/SuperFeda/aioheleket/tree/master/examples)

- [RU README](https://github.com/SuperFeda/aioheleket/blob/master/readme/ru-readme.md)

### pip
```shell
pip install aioheleket
```

### uv
```shell
uv pip install aioheleket
```

# Documentation
[Official Heleket documentation](https://doc.heleket.com).

A quick start guide is provided at the bottom of this README, and the library also includes docstrings.

# Features

## Creating a payment

```python
import asyncio

from aioheleket import HeleketClient, CryptoCurrency, Network, Lifetime


async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>"
    )
    payment_service = await client.payment_service()
    
    payment = await payment_service.create_invoice(
        currency=CryptoCurrency.USDT,
        network=Network.ETH,
        order_id="order_3331",
        amount="2",
        lifetime=Lifetime.HOUR_5
    )
    print(payment.url, payment.uuid, payment.address)

    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

## Transferring funds from a business wallet to a personal wallet

```python
import asyncio

from aioheleket import HeleketClient, CryptoCurrency


async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payout_api_key="<payout_api_key>"
    )
    payout_service = await client.payout_service()
    
    transfer = await payout_service.transfer_to_personal_wallet(
        currency=CryptoCurrency.USDT,
        amount="4"
    )
    print(transfer.user_wallet_transaction_uuid, transfer.user_wallet_balance)

    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

## Creating a static wallet

```python
import asyncio

from aioheleket import HeleketClient, Network, CryptoCurrency


async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>"
    )
    wallet_service = await client.static_wallet_service()
    
    wallet = await wallet_service.create_wallet(
        currency=CryptoCurrency.USDT,
        network=Network.ETH,
        order_id="wal_usdt"
    )
    print(wallet.uuid, wallet.url)

    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

## Viewing balance

```python
import asyncio

from aioheleket import HeleketClient


async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>"
    )
    finance_service = await client.finance_service()

    balance = await finance_service.balance()

    print("--- User balance")
    for i, balance_info in enumerate(balance.user, 1):
        print(f"{i}) {balance_info.currency_code}\nAmount: {balance_info.crypto_balance}\nAmount in USD: {balance_info.usd_balance}\nUUID: {balance_info.uuid}\n")

    print("\n--- Merchant balance")
    for i, balance_info in enumerate(balance.merchant, 1):
        print(f"{i}) {balance_info.currency_code}\nAmount: {balance_info.crypto_balance}\nAmount in USD: {balance_info.usd_balance}\nUUID: {balance_info.uuid}\n")

    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

## Getting exchange rates

```python
import asyncio

from aioheleket import HeleketClient, CryptoCurrency, FiatCurrency


async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>"
    )
    finance_service = await client.finance_service()
    
    print("--- BTC exchange rates for RUB, KZT, and TRX")
    target_currencies = (FiatCurrency.RUB, CryptoCurrency.TRX, FiatCurrency.KZT)
    btc_rate = await finance_service.exchange_rate(CryptoCurrency.BTC, target_currencies)
    for i, rate in enumerate(btc_rate, 1):
        print(f"{i}) {rate.to}: {rate.course}")
    
    print("\n--- All BTC exchange rates")
    all_btc_rates = await finance_service.exchange_rate(CryptoCurrency.BTC)
    for i, rate in enumerate(all_btc_rates, 1):  # output all rates for BTC
        print(f"{i}) {rate.to}: {rate.course}")

    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

## The `async with` usage

```python
import asyncio

from aioheleket import HeleketClient, CryptoCurrency, FiatCurrency


async def main() -> None:
    async with HeleketClient(
            merchant_id="<merchant_id>", 
            payment_api_key="<payment_api_key>"
    ) as client:
        finance_service = await client.finance_service()
        ...


if __name__ == "__main__":
    asyncio.run(main())
```

# Quick start

To create a client instance, you must pass `merchant_id` and API keys: `payout_api_key`, `payment_api_key` to `aioheleket.HeleketClient`.

If you need to customize request handling within the library, you can use `aioheleket.RequestConfig`, [more details](https://github.com/SuperFeda/aioheleket/tree/master/examples/request_config_usage.py).

```python
import asyncio

from aioheleket import HeleketClient


async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payout_api_key="<payout_api_key>",
        payment_api_key="<payment_api_key>"
    )
    ...

    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

Before starting to work with the Heleket API, you need to create a service that will interact with a <u>specific</u> Heleket entity. To do this, access the client instance and call the corresponding method:

- `payment_service() -> PaymentService` - service for working with payments. (`payment_api_key` is required)
- `payout_service() -> PayoutService` - service for working with payouts. (`payout_api_key` is required)
- `static_wallet_service() -> StaticWalletService` - service for interacting with a static wallet. (`payment_api_key` is required)
- `finance_service() -> FinanceService` - service for retrieving balance and exchange rate data. (`payment_api_key` is required)

Example with `payment_service` and [creating a new invoice](https://doc.heleket.com/en/methods/payments/creating-invoice):

```python
import asyncio

from aioheleket import HeleketClient


async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>"
    )
    payment_service = await client.payment_service()
    
    payment = await payment_service.create_invoice(
        amount="2",
        currency="USDT",
        network="ETH",
        order_id="orderid_2usdt",
        lifetime=5_000
    )
    print(payment)
    
    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

> [!NOTE]
> Keep in mind that when accessing the same client and repeatedly creating the same service, you will be returned the service instance that was created the very first time.

> [!IMPORTANT]
> All returned objects are immutable Pydantic models. You cannot modify their attributes or create instances with incomplete data.

By the way, you don't have to create all services at once, nor do you have to pass all API keys to `HeleketClient`. If you only need to work with one specific entity, for example payouts, then you can pass only `payout_api_key` to `HeleketClient` and create only `payout_service`. (Similar to the example above, but there it's payment instead of payout.)

Which API key is required for a specific service was described just above, before the payment creation example.