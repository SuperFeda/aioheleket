import asyncio

from aioheleket import HeleketClient


async def main() -> None:
    client = HeleketClient(
        merchant_id="",
        payment_api_key="",
        payout_api_key=""
    )
    payment_service = await client.payment_service()
    payout_service = await client.payout_service()

    print("Payout services info : ")
    for service in await payout_service.services_info():
        print(service)
    print()
    print("Payment services info : ")
    for service in await payment_service.services_info():
        print(service)

    await client.close_session()


if __name__ == "__main__":
    asyncio.run(main())
