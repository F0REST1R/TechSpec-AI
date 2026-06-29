from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu(is_admin: bool = False) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="🚀 Создать новое ТЗ",
                callback_data="create_tz",
            ),
        ],
        [
            InlineKeyboardButton(
                text="📁 Мои проекты",
                callback_data="projects",
            ),
            InlineKeyboardButton(
                text="ℹ️ Инструкция",
                callback_data="info",
            ),
        ],
    ]

    if is_admin:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="📢 Сделать рассылку",
                    callback_data="mailing",
                ),
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
back_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="back_menu",
            )
        ]
    ]
)