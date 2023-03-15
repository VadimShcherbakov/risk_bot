from dataclasses import dataclass
from environs import Env
from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot


class CorrectInputRisk(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        pattern = r"(\d{1,2})-(\d{1,3})-([12])"
        strings = message.text
        if re.fullmatch(pattern, strings):
            print("нашел")
            return {'num_risk': strings}
        return False


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))