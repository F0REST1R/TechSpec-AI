from aiogram import F, Router
from aiogram.types import CallbackQuery
from app.handlers.start import start


router = Router()

@router.callback_query(F.data == "back_menu")
async def back_menu(callback: CallbackQuery):
    await callback.message.delete()
    await start(callback.message)
    await callback.answer()