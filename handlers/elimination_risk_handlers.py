from aiogram import Router
from aiogram.filters import  StateFilter
from aiogram.fsm.context import FSMContext
from config_data.config import CorrectInputNumRisk, FSMFillForm
from lexicon.lexicon_ru import LEXICON_RU
from aiogram import F
from aiogram.types import Message

router: Router = Router()


# Этот хэндлер будет срабатывать, если введен корректный номер риска обнулять состояние
@router.message(StateFilter(FSMFillForm.fill_num_risk), F.text, CorrectInputNumRisk())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON_RU['accepted_review_answer'])
    print(message.text)
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если во время ввода номера риска
# будет введено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_num_risk))
async def warning_not_name(message: Message):
    await message.answer(text=LEXICON_RU['enter_elimination_risk_num_err_answer'])