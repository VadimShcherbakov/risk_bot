from typing import Any
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, PhotoSize
from aiogram.filters import BaseFilter, Text
import re

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
API_TOKEN: str = '5443763132:AAHwrgf4WPPFBOXl9Gs1HL6ejTsO4-wgWAk'

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

# Этот фильтр будет проверять наличие неотрицательных чисел
# в сообщении от пользователя, и передавать в хэндлер их список
class CorrectInputRisk(BaseFilter):
    async def __call__(self, message: Message) -> bool | dict[str, list[int]]:
        pattern = r"(\d{1,2})-(\d{1,3})-([12])"
        strings = message.text
        if re.fullmatch(pattern, strings):
            print("нашел")
            return {'num_risk': strings}
        return False

# Этот хэндлер будет срабатывать, если сообщение пользователя
# начинается с фразы "найди числа" и в нем есть числа
@dp.message(CorrectInputRisk())
# Помимо объекта типа Message, принимаем в хэндлер список чисел из фильтра
async def process_if_numbers(message: Message, num_risk: dict):
    await message.answer(text=f'Нашел: {num_risk}')

@dp.message(F.photo[0].as_('photo_min'))
async def process_photo_send(message: Message, photo_min: PhotoSize):
    print(photo_min)

@dp.message()
async def send_echo(message: Message):
        await message.answer(text="Введите номер риска по образцу: 1-300-1")
        print(message.text)

if __name__ == '__main__':
    dp.run_polling(bot)
