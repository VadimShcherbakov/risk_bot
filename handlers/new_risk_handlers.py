from aiogram import Router
from aiogram.filters import Command, CommandStart, Text, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from config_data.config import CorrectInputNumRisk, FSMFillForm
from keyboards.keyboards import new_elimination_risk_kb
from lexicon.lexicon_ru import LEXICON_RU
from aiogram import F
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)

router: Router = Router()


# Этот хэндлер будет срабатывать, если введены корректные координаты
# только из буквенно-цифровых символов и переводить обнулять состояние
@router.message(StateFilter(FSMFillForm.fill_input_location_risk), F.text)
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON_RU['accepted_review_answer'])
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если во время ввода координат риска
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_input_location_risk))
async def warning_not_name(message: Message):
    await message.answer(text=LEXICON_RU['enter_new_risk_location_err_answer'])