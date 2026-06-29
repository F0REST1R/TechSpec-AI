from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.config import config

from app.keyboards.main_menu import get_main_menu

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
        reply_markup=get_main_menu(
            is_admin=message.from_user.id in config.admin_ids
        ),
    )