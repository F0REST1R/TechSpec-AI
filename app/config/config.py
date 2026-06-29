from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Config:
    bot_token: str
    deepseek_api: str
    admin_ids: list[int]


config = Config(
    bot_token=os.getenv("BOT_TOKEN", ""),
    deepseek_api=os.getenv("DEEPSEEK_API", ""),
    admin_ids=[
        int(admin_id)
        for admin_id in os.getenv("ADMIN_IDS", "").split(",")
        if admin_id.strip()
    ],
)

if not config.bot_token:
    raise ValueError("BOT_TOKEN not found in .env")

if not config.deepseek_api:
    raise ValueError("DEEPSEEK_API not found in .env")