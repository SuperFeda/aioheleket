import asyncio

from typing import Optional
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aioheleket import HeleketClient
from aioheleket.services import PaymentService

from handlers.routers import client
from handlers.utils import async_partial


class CryptoBot(Bot):
    def __init__(
            self,
            token: str,
            default: Optional[DefaultBotProperties] = None,
            payment_service: Optional[PaymentService] = None
    ) -> None:
        self.payment_service = payment_service
        super().__init__(token=token, default=default)


async def startup() -> None:
    print("Bot started")


async def shutdown(heleket_client: HeleketClient) -> None:
    print("Bot shutdown")
    await heleket_client.close_session()


async def main() -> None:
    # <!> for merchant_id, payment_api_key and bot token use os.getenv()

    heleket = HeleketClient(
        merchant_id="your_merchant_id",
        payment_api_key="your_payment_api_key"
    )
    payment_service = await heleket.payment_service()

    bot = CryptoBot(
        token="your_bot_token",
        default=DefaultBotProperties(parse_mode="Markdown"),
        payment_service=payment_service
    )

    dp = Dispatcher()
    dp.shutdown.register(async_partial(shutdown, heleket))
    dp.startup.register(startup)
    dp.include_routers(client.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
