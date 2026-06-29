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
Описание проекта

{description}


Во время интервью пользователь ответил следующим образом:

{interview}


На основании всей информации составь максимально подробное техническое задание.

Документ обязательно должен содержать следующие разделы.

# 1. Общая информация о проекте

Опиши проект.

---

# 2. Цель проекта

---

# 3. Целевая аудитория

---

# 4. Роли пользователей

Если ролей нет — напиши.

---

# 5. Функциональные требования

Максимально подробно.

Каждую функцию отдельным подпунктом.

---

# 6. Пользовательские сценарии

Например:

Регистрация

Авторизация

Создание проекта

Редактирование

Удаление

и т.д.

---

# 7. Нефункциональные требования

Производительность

Безопасность

Надежность

Масштабируемость

---

# 8. Требования к интерфейсу

---

# 9. Интеграции

---

# 10. Ограничения

---

# 11. Дополнительные пожелания

---

# 12. Возможные риски

---

# 13. Этапы разработки

Разбей проект на логичные этапы.

---

# 14. Критерии приемки

Опиши, как понять, что проект выполнен.

---

Документ должен быть очень подробным.

Минимум 2500 слов.

Используй Markdown.
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