from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text == "ℹ️ Информация")
async def info(message: Message):
    await message.answer(
        "Этот бот помогает автоматически составить техническое "
        "задание для разработки.\n\n"
        "Как это работает:\n"
        "• Вы описываете свою идею;\n"
        "• Бот задаёт уточняющие вопросы;\n"
        "• AI анализирует ответы;\n"
        "• Вы получаете готовое ТЗ в PDF."
    )