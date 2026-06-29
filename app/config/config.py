from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Config:
    bot_token: str = os.getenv("BOT_TOKEN", "")


config = Config()

if not config.bot_token:
    raise ValueError("BOT_TOKEN not found in .env")