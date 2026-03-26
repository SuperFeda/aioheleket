# aioheleket

Асинхронная Python библиотека для API криптоплатежей [Heleket](https://heleket.com).

[Примеры использования](https://github.com/SuperFeda/aioheleket/tree/master/examples)

### pip
```shell
pip install aioheleket
```

### uv
```shell
uv pip install aioheleket
```

# Документация
[Официальная документация Heleket](https://doc.heleket.com).

Внизу README находится инструкция по быстрому старту, также в библиотеке прописаны докстринги.

# Фичи

## Создание платежа

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

## Перевод денег из бизнес кошелька на персональный

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

## Создание статического кошелька

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

## Просмотр баланса

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

    print("--- Баланс пользователя")
    for i, balance_info in enumerate(balance.user, 1):
        print(f"{i}) {balance_info.currency_code}\nСумма: {balance_info.crypto_balance}\nСумма в USD: {balance_info.usd_balance}\nUUID: {balance_info.uuid}\n")

    print("\n--- Баланс мерчанта")
    for i, balance_info in enumerate(balance.merchant, 1):
        print(f"{i}) {balance_info.currency_code}\nСумма: {balance_info.crypto_balance}\nСумма в USD: {balance_info.usd_balance}\nUUID: {balance_info.uuid}\n")

    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

## Получение обменных курсов

```python
import asyncio

from aioheleket import HeleketClient, CryptoCurrency, FiatCurrency


async def main() -> None:
    client = HeleketClient(
        merchant_id="<merchant_id>",
        payment_api_key="<payment_api_key>"
    )
    finance_service = await client.finance_service()
    
    print("--- Обменные курсы BTC для RUB, KZT и TRX")
    target_currencies = (FiatCurrency.RUB, CryptoCurrency.TRX, FiatCurrency.KZT)
    btc_rate = await finance_service.exchange_rate(CryptoCurrency.BTC, target_currencies)
    for i, rate in enumerate(btc_rate, 1):
        print(f"{i}) {rate.to}: {rate.course}")
    
    print("\n--- Все обменные курсы BTC")
    all_btc_rates = await finance_service.exchange_rate(CryptoCurrency.BTC)
    for i, rate in enumerate(all_btc_rates, 1):  # вывод всех курсов для BTC
        print(f"{i}) {rate.to}: {rate.course}")

    await client.close_session()  # <!>


if __name__ == "__main__":
    asyncio.run(main())
```

## Использование контекстного менеджера

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

# Быстрый старт

Для создания экземпляра клиента обязательно передать `merchant_id` и API ключи: `payout_api_key`, `payment_api_key` в `aioheleket.HeleketClient`. 

Если нужно по своему настроить обработку запросов внутри библиотеки, то можно воспользоваться `aioheleket.RequestConfig`, [подробнее](https://github.com/SuperFeda/aioheleket/tree/master/examples/request_config_usage.py).

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

Перед началом работы с API Heleket нужно создать сервис, с помощью которого будет происходить взаимодействие с <u>определенной</u> сущностью Heleket. Чтобы сделать это, нужно обратиться к экземпляру клиента и вызвать соответсвующий метод:

- `payment_service() -> PaymentService` - сервис для работы с платежами. (Обязательно наличие `payment_api_key`)
- `payout_service() -> PayoutService` - сервис для работы с выплатами. (Обязательно наличие `payout_api_key`)
- `static_wallet_service() -> StaticWalletService` - сервис для взаимодействия со статическим кошельком. (Обязательно наличие `payment_api_key`)
- `finance_service() -> FinanceService` - сервис для получения данных о балансе и обменных курсах. (Обязательно наличие `payment_api_key`)

Пример с `payment_service` и [созданием нового платежа](https://doc.heleket.com/ru/methods/payments/creating-invoice):

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
> Имейте в виду, что при обращении к одному и тому же клиенту и многократном создании одного и того же сервиса вам будет возвращаться тот экземпляр сервиса, что был создан в самый первый раз. 

> [!IMPORTANT]
> Все возвращаемые объекты - это неизменяемые Pydantic модели. Вы не можете изменять их атрибуты или создавать экземпляры с неполными данными. 

К слову, вам не обязательно создавать все сервисы сразу, так же как не обязательно передавать все API ключи в `HeleketClient`. Если вам требуется работать только с одной определенной сущностью, например с выплатами (payout), то в этом случае в `HeleketClient` можно передать только `payout_api_key` и создать только `payout_service`. (Подобно примеру выше, только там вместо payout работа с payment.)

Какой API ключ нужен для конкретного сервиса было описано чуть выше, перед примером с созданием платежа.

