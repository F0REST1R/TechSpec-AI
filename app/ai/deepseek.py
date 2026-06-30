import json

from openai import AsyncOpenAI

from .prompts import SYSTEM_PROMPT
from app.config import config


client = AsyncOpenAI(
    api_key=config.deepseek_api,
    base_url="https://api.deepseek.com/v1",
)


async def generate_questions(description: str) -> list[str]:
    prompt = f"""
Ты профессиональный бизнес-аналитик.

Пользователь описал проект.

Описание:

{description}

Твоя задача:

Определи, какой информации не хватает.

Составь 5 вопросов.

Правила:

- не спрашивай очевидное;
- вопросы должны идти в логическом порядке;
- только важные вопросы;
- не задавай сразу несколько вопросов в одном.

Ответ верни ТОЛЬКО в JSON.

Формат:

{{
    "questions":[
        "...",
        "...",
        "..."
    ]
}}
"""

    response = await client.chat.completions.create(
        model="deepseek-chat",
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Ты опытный системный аналитик.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    data = json.loads(response.choices[0].message.content)

    return data["questions"]

async def generate_specification(
    description: str,
    questions: list[str],
    answers: list[str],
) -> str:

    interview = ""

    for i, (question, answer) in enumerate(zip(questions, answers), start=1):
        interview += (
            f"\nВопрос {i}:\n"
            f"{question}\n\n"
            f"Ответ:\n"
            f"{answer}\n"
        )

    prompt = f"""
    Ты Senior System Analyst.

    Твоя задача — написать профессиональное техническое задание.

    Ни в коем случае не придумывай информацию.

    Если информации нет —
    напиши

    Не определено.

    ========================

    Описание проекта

    {description}

    ========================

    Во время интервью были получены ответы.

    """

    for i, (q, a) in enumerate(zip(questions, answers), start=1):

        prompt += f"""

    Вопрос {i}

    {q}

    Ответ

    {a}

    """
    
    prompt += """

    ========================

    Составь полноценное техническое задание.

    Используй Markdown.

    Структура документа.


    # Общая информация

    Опиши проект.


    # Цель проекта


    # Пользователи


    # Роли пользователей


    # Основные сценарии использования


    # Функциональные требования

    Максимально подробно.

    Разбей по разделам.

    Используй списки.

    Для каждого функционала подробно опиши поведение.


    # Административная панель

    Если требуется.


    # Требования к интерфейсу


    # Интеграции


    # API

    Если необходимо.


    # Нефункциональные требования

    Производительность

    Безопасность

    Надежность

    Логирование

    Масштабируемость


    # Ограничения


    # Возможные ошибки


    # Этапы разработки


    # Критерии приемки


    # Заключение


    Документ должен выглядеть как настоящее ТЗ.

    Пиши максимально подробно.

    Используй профессиональную терминологию.

    Минимум воды.

    """

    response = await client.chat.completions.create(
        model="deepseek-chat",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content