from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile
from app.ai.deepseek import generate_questions, generate_specification

from app.keyboards.main_menu import back_menu
from app.states.create_tz import CreateTZ
from app.pdf.generator import create_pdf
from pathlib import Path

router = Router()


@router.callback_query(F.data == "create_tz")
async def create_tz(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.clear()
    await state.set_state(CreateTZ.waiting_description)

    await callback.message.delete()

    await callback.message.answer(
        "🚀 <b>Создание технического задания</b>\n\n"
        "Опишите максимально подробно ваш проект.\n\n"
        "Например:\n"
        "• Что необходимо разработать?\n"
        "• Для кого предназначен продукт?\n"
        "• Какие основные функции должны быть?\n"
        "• Есть ли пожелания по дизайну?\n"
        "• Нужны ли интеграции?\n\n"
        "💡 Не переживайте, если что-то забудете — позже я задам уточняющие вопросы.",
        parse_mode="HTML",
        reply_markup=back_menu,
    )


@router.message(CreateTZ.waiting_description)
async def get_description(message: Message, state: FSMContext):
    description = message.text.strip()

    if len(description) < 30:
        await message.answer(
            "❗ Опишите проект немного подробнее (минимум 30 символов)."
        )
        return

    await state.update_data(
        description=description,
        questions=[],
        answers=[],
        current_question=0,
    )

    await state.set_state(CreateTZ.generating)

    questions = await generate_questions(description)

    await state.update_data(
        description=description,
        questions=questions,
        answers=[],
        current_question=0,
    )

    await state.set_state(CreateTZ.answering_questions)

    await message.answer(
        f"❓ Вопрос 1 из {len(questions)}\n\n"
        f"{questions[0]}",
        reply_markup=back_menu,
    )

@router.message(CreateTZ.answering_questions)
async def answer_question(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()

    questions = data["questions"]
    answers = data["answers"]
    current = data["current_question"]

    answers.append(message.text.strip())

    current += 1

    if current >= len(questions):

        await state.update_data(
            answers=answers,
            current_question=current,
        )

        await state.set_state(CreateTZ.generating)

        data = await state.get_data()

        await message.answer(
            "🧠 Анализирую ответы..."
        )

        specification = await generate_specification(
            description=data["description"],
            questions=data["questions"],
            answers=data["answers"],
        )

        await message.answer(
            "📄 Формирую PDF..."
        )

        filename = f"tz_{message.from_user.id}.pdf"

        pdf_path = create_pdf(
            specification,
            filename,
        )

        await message.answer_document(
            document=FSInputFile(pdf_path),
            caption="✅ Техническое задание успешно сформировано.",
        )

        Path(pdf_path).unlink(missing_ok=True)

        await state.clear()

        return

    await state.update_data(
        answers=answers,
        current_question=current,
    )

    await message.answer(
        f"<b>Вопрос {current + 1} из {len(questions)}</b>\n\n"
        f"{questions[current]}",
        parse_mode="HTML",
        reply_markup=back_menu,
    )