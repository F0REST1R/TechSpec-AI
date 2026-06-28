from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.main_menu import main_menu

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    text = (
        "👋 Добро пожаловать!\n\n"
        "Я помогу составить качественное техническое задание.\n\n"
        "Опишите вашу идею, а я задам необходимые вопросы "
        "и сформирую профессиональное ТЗ."
    )

    await message.answer(
        text=text,
        reply_markup=main_menu,
    )