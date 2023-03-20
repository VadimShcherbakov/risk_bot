from dataclasses import dataclass
from environs import Env
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
import re


@dataclass
class MailConfig:
    mail_user: str          # Username пользователя базы данных
    mail_password: str      # Пароль к базе данных


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBot
    mail_data: MailConfig



# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_input_move = State()  # Состояние ожидания ввода действия ('Отправка нового риска','Устранение риска')
    fill_input_location_risk = State()  # Состояние ожидания ввода координат риска
    fill_num_risk = State()   # Состояние ожидания ввода номера риска


class CorrectInputNumRisk(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        pattern = r"(\d{1,2})-(\d{1,3})-([12])"
        strings = message.text
        if re.fullmatch(pattern, strings):
            return {'num_risk': strings}
        return False


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  mail_data=MailConfig(mail_user=env('MAIL'),
                                       mail_password=env('MAIL_PASSWORD'))
                  )