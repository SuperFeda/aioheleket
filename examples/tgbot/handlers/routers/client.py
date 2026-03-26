from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aioheleket import Lifetime, PaymentStatus
from datetime import datetime

import handlers.keyboards as kb

from handlers.products import products

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message) -> None:
    await message.answer("Welcome!", reply_markup=kb.see_products_kb)


@router.callback_query(F.data == "products")
async def products_page(callback: CallbackQuery) -> None:
    await callback.message.edit_text("all products:", reply_markup=await kb.products_kb())


@router.callback_query(F.data.startswith("product-info"))
async def product_info(callback: CallbackQuery) -> None:
    product_data = products.get(callback.data.split(":")[1])
    bot = callback.bot
    order_id = f"order_{callback.from_user.username}_{product_data.get('name')}_{datetime.now().strftime('%d-%m-%Y')}"
    payment = await bot.payment_service.create_invoice(
        amount=product_data.get("price"),
        currency=product_data.get("currency"),
        network=product_data.get("network"),
        order_id=order_id,
        lifetime_sec=Lifetime.HOUR_3
    )
    await callback.message.edit_text(
        f"{product_data.get('name')}({product_data.get('price')} {product_data.get('currency')})\n\n{product_data.get('description')}",
        reply_markup=await kb.payment_kb(url=payment.url, order_id=order_id)
    )


@router.callback_query(F.data.startswith("check-payment"))
async def check_payment(callback: CallbackQuery) -> None:
    order_id = callback.data.split(":")[1]
    payment_info = await callback.bot.payment_service.payment_info(order_id=order_id)
    if payment_info.status == PaymentStatus.PAID:
        await callback.message.answer("Paid!!!!")
    else:
        await callback.message.answer("Not paid")

