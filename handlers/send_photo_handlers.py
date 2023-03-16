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


# Этот хэндлер будет срабатывать, если отправлено фото
# и переводить в состояние выбора действия
@router.message(F.photo[-1].as_('largest_photo'), StateFilter(default_state))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             largest_photo: PhotoSize):
    # Cохраняем данные фото (file_unique_id и file_id) в хранилище
    # по ключам "photo_unique_id" и "photo_id"
    await state.update_data(photo_unique_id=largest_photo.file_unique_id,
                            photo_id=largest_photo.file_id)

    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text=LEXICON_RU['select_move_answer'],
                         reply_markup=new_elimination_risk_kb)
    # Устанавливаем состояние ожидания выбора действия с риском
    await state.set_state(FSMFillForm.fill_input_move)






