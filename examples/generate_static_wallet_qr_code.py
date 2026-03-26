import asyncio

from aioheleket import (
    HeleketClient,
    CryptoCurrency,
    Network
)


async def main() -> None:
    client = HeleketClient(
        merchant_id="",
        payment_api_key="",
    )
    static_wallet_service = await client.static_wallet_service()

    wallet = await static_wallet_service.create_wallet(
        currency=CryptoCurrency.ETH,
        network=Network.ETH,
        order_id="wallet_order_id",
    )
    qr = await static_wallet_service.generate_qr_code(wallet.uuid)
    print(qr)

    await client.close_session()


if __name__ == "__main__":
    asyncio.run(main())
