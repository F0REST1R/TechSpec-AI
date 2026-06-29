from aiogram import F, Router
from aiogram.types import CallbackQuery
from app.keyboards.main_menu import back_menu
router = Router()


@router.callback_query(F.data == "info")
async def instruction(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "📖 <b>Как пользоваться TechSpec AI</b>\n\n"
        "1. Нажмите <b>«🚀 Создать новое ТЗ»</b>.\n"
        "2. Кратко опишите ваш проект или идею.\n"
        "3. Ответьте на вопросы бота — они помогут собрать все необходимые требования.\n"
        "4. AI обработает полученную информацию и сформирует техническое задание.\n"
        "5. Через несколько секунд вы получите готовый PDF-документ.\n\n"
        "📄 В ТЗ будут включены:\n"
        "• описание проекта;\n"
        "• цели и задачи;\n"
        "• функциональные требования;\n"
        "• требования к дизайну;\n"
        "• технические требования;\n"
        "• дополнительные пожелания;\n"
        "• рекомендации по реализации.\n\n"
        "💡 Чем подробнее вы отвечаете на вопросы, тем качественнее получится итоговое техническое задание.",
        parse_mode="HTML", reply_markup=back_menu
    )

    await callback.answer()