from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Создать ТЗ"),
        ],
        [
            KeyboardButton(text="📂 Мои проекты"),
            KeyboardButton(text="ℹ️ Информация"),
        ],
    ],
    resize_keyboard=True,
)