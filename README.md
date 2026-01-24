# aioheleket

An asynchronous Python library for the [Heleket](https://heleket.com) cryptocurrency payment API.

[See examples](https://github.com/SuperFeda/aioheleket-examples)

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
[Official Heleket Documentation](https://doc.heleket.com).

The library also includes docstrings.

# Features

## Creating a Client

```python
import asyncio

from aioheleket import HeleketClient

async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>",
        payout_api_key="<payout_api_key>"
    )

    await client.close_session()  # <!>

if __name__ == "__main__":
    asyncio.run(main())
```

## Creating a Payment

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

## Transferring Money from Business Wallet to Personal Wallet

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

## Creating a Static Wallet

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

## Viewing Balance

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

    print("--- User Balance")
    for i, balance_info in enumerate(balance.user, 1):
        print(f"{i}) {balance_info.currency_code}\nAmount: {balance_info.crypto_amount}\nAmount in USD: {balance_info.usd_amount}\nUUID: {balance_info.uuid}\n")

    print("\n--- Merchant Balance")
    for i, balance_info in enumerate(balance.merchant, 1):
        print(f"{i}) {balance_info.currency_code}\nAmount: {balance_info.crypto_amount}\nAmount in USD: {balance_info.usd_amount}\nUUID: {balance_info.uuid}\n")

    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

## Getting Exchange Rates

```python
import asyncio

from aioheleket import HeleketClient, CryptoCurrency, FiatCurrency


async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>"
    )
    finance_service = await client.finance_service()
    
    print("--- BTC Exchange Rates for RUB, KZT, and TRX")
    target_currencies = (FiatCurrency.RUB, CryptoCurrency.TRX, FiatCurrency.KZT)
    btc_rate = await finance_service.exchange_rate(CryptoCurrency.BTC, target_currencies)
    for i, rate in enumerate(btc_rate, 1):
        print(f"{i}) {rate.to}: {rate.course}")
    
    print("\n--- All BTC Exchange Rates")
    all_btc_rates = await finance_service.exchange_rate(CryptoCurrency.BTC)
    for i, rate in enumerate(all_btc_rates, 1):  # output all rates for BTC
        print(f"{i}) {rate.to}: {rate.course}")

    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

