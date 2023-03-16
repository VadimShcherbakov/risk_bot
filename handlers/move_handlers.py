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


# Этот хэндлер будет срабатывать, если выбрано действие "Отправка нового риска"
# и переводить в состояние ввода координат риска
@router.callback_query(StateFilter(FSMFillForm.fill_input_move),
                       Text(text=['new_risk']))
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['enter_new_risk_answer'])
    # Устанавливаем состояние ожидания ввода координат риска
    await state.set_state(FSMFillForm.fill_input_location_risk)


# Этот хэндлер будет срабатывать, если выбрано действие "Устранение риска"
# и переводить в состояние ввода координат риска
@router.callback_query(StateFilter(FSMFillForm.fill_input_move),
                       Text(text=['elimination_risk']))
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['enter_num_risk_answer'])
    # Устанавливаем состояние ожидания ввода номера риска
    await state.set_state(FSMFillForm.fill_num_risk)


# Этот хэндлер будет срабатывать, если во время выбора действия
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_input_move))
async def warning_not_gender(message: Message):
    await message.answer(text=LEXICON_RU['text_err_input_move'],
                         reply_markup=new_elimination_risk_kb)