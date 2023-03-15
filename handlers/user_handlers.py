from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message

from config_data.config import CorrectInputRisk
from keyboards.keyboards import new_elimination_risk_kb
from lexicon.lexicon_ru import LEXICON_RU
from aiogram import F

router: Router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер срабатывает на отправку пользователем фото риска
@router.message(F.photo)
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['select_move_answer'], reply_markup=new_elimination_risk_kb)
    # await message.answer(text=LEXICON_RU['enter_num_risk_answer'] )
    # @router.message(CorrectInputRisk())
    # # Помимо объекта типа Message, принимаем в хэндлер список чисел из фильтра
    # async def process_if_numbers(message: Message, num_risk: dict):
    #     await message.answer(text=f'Нашел: {num_risk}')

# Этот хэндлер срабатывает на нажатие кнопки "Отправка нового риска"
@router.message(Text(text=LEXICON_RU['new_risk_button']))
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['enter_new_risk_answer'])

    @router.message()
    async def send_answer(message: Message):
        await message.answer(text=LEXICON_RU['accepted_review_answer'])
        print("успех")


