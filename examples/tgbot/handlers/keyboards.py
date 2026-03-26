from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder
)

from handlers.products import products


see_products_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="See products", callback_data="products")
]])


async def products_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for _, pr in products.items():
        kb.row(InlineKeyboardButton(text=pr.get("name"), callback_data=f"product-info:{pr.get('name')}"))

    return kb.as_markup()


async def payment_kb(url: str, order_id: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Pay", url=url)
    kb.button(text="Check status", callback_data=f"check-payment:{order_id}")
    kb.button(text="back", callback_data="products")

    return kb.adjust(1).as_markup()

