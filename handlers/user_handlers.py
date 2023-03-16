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


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel_in_status'])
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['/cancel_without_status'])


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


# Этот хэндлер будет срабатывать, если во время выбора действия
# будет введено/отправлено что-то некорректное
@router.message(StateFilter(FSMFillForm.fill_input_move))
async def warning_not_gender(message: Message):
    await message.answer(text=LEXICON_RU['text_err_input_move'],
                         reply_markup=new_elimination_risk_kb)


# Этот хэндлер будет срабатывать, если выбрано действие "Отправка нового риска"
# и переводить в состояние ввода координат риска
@router.callback_query(StateFilter(FSMFillForm.fill_input_move),
                       Text(text=['new_risk']))
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['enter_new_risk_answer'])
    # Устанавливаем состояние ожидания ввода координат риска
    await state.set_state(FSMFillForm.fill_input_location_risk)


# Этот хэндлер будет срабатывать, если введено корректные координаты
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



