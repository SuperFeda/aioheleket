import asyncio

from aioheleket import HeleketClient


async def main() -> None:
    client = HeleketClient(
        merchant_id="",
        payment_api_key=""
    )
    payment_service = await client.payment_service()

    payment_history = await payment_service.payment_history()
    print(f"{payment_history.paginate = }")
    for payment in payment_history.items:
        print(payment)

    await client.close_session()


if __name__ == "__main__":
    asyncio.run(main())
