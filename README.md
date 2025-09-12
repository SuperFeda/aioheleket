# aioheleket

<p align="center">
<a href="https://heleket.com">
<img width="637" height="136" alt="Heleket logo" src="https://github.com/user-attachments/assets/cb02eb9d-8fca-40e8-8437-9fd04b5970dd" />
</a>
</p>

Asynchronous Python library for [Heleket](https://heleket.com) crypto payments.

### pip
```shell
pip install git+https://github.com/SuperFeda/aioheleket.git@master
```

### uv
```shell
uv pip install git+https://github.com/SuperFeda/aioheleket.git@master
```

# Documentation
[Official Heleket documentation](https://doc.heleket.com)

# Features

[See examples](https://github.com/SuperFeda/aioheleket-examples)

## Creating payment

```python
import asyncio

from aioheleket import HeleketClient, Currency, Network, Lifetime

async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>"
    )
    payment_service = await client.payment()
    payment = await payment_service.create_invoice(
        currency=Currency.USDT,
        network=Network.ETH,
        order_id="order_3331",
        amount="2",
        lifetime_sec=Lifetime.HOUR_2
    )
    print(payment.url, payment.uuid)

    await client.close_session()  # <!>

if __name__ == "__main__":
    asyncio.run(main())
```

## Transfer funds from a business wallet to a personal wallet
```python
import asyncio

from aioheleket import HeleketClient, Currency

async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payout_api_key="<payout_api_key>"
    )
    payout_service = await client.payout()
    transfer = await payout_service.personal_transfer(
        currency=Currency.USDT,
        amount="4"
    )
    print(transfer.user_wallet_transaction_uuid, transfer.user_wallet_balance)
    
    await client.close_session()  # <!>
    
if __name__ == "__main__":
    asyncio.run(main())
```

## Creating static wallet

```python
import asyncio

from aioheleket import HeleketClient, Network, Currency

async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>"
    )
    wallet_service = await client.static_wallet()
    wallet = await wallet_service.create(
        currency=Currency.USDT,
        network=Network.ETH,
        order_id="wal_7342"
    )
    print(wallet.uuid, wallet.url)
    
    await client.close_session()  # <!>
    
if __name__ == "__main__":
    asyncio.run(main())
```

## Get the current exchange rate
```python
import asyncio

from aioheleket import HeleketClient, Currency

async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>"
    )
    finance_service = await client.finance()
    rates = await finance_service.exchange_rate(Currency.BTC, ("RUB", Currency.TRX, "KZT"))
    print(rates)  # output BTC exchange rate only for RUB, KZT, TRX
    all_rates = await finance_service.exchange_rate(Currency.BTC)
    print(all_rates)  # output all exchange rate for BTC
    
    await client.close_session()  # <!>
    
if __name__ == "__main__":
    asyncio.run(main())
```


# Support
ETH `0x4837EFA4AF3F4f09BFd96Ed964f4Bd2CBf71Ce53`</br>
BTC `bc1qu2vsd8duengpqexc5d6f87cenqfcwv74lynr4x`</br>
USDT (ERC20) `0x4837EFA4AF3F4f09BFd96Ed964f4Bd2CBf71Ce53`</br>
