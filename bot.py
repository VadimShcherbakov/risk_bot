from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, PhotoSize)
from config_data.config import *
from keyboards.keyboards import *
from services.mail import mail
import os

# Загружаем конфиг в переменную config
config: Config = load_config()

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: MemoryStorage = MemoryStorage()

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp: Dispatcher = Dispatcher()

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}


# Этот хэндлер срабатывает на команду /start
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер срабатывает на команду /help
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel_in_status'])
    # Сбрасываем состояние
    await state.clear()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда доступна в машине состояний
@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['/cancel_without_status'])


# Этот хэндлер будет срабатывать, если отправлено фото
# и переводить в состояние выбора действия
@dp.message(F.photo[-1].as_('largest_photo'), StateFilter(default_state))
async def process_photo_sent(message: Message,
                             state: FSMContext,
                             largest_photo: PhotoSize):
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(text=LEXICON_RU['select_move_answer'],
                         reply_markup=new_elimination_risk_kb)
    # Cохраняем данные фото (file_unique_id и file_id) в хранилище
    # по ключам "photo_unique_id" и "photo_id"
    await state.update_data(photo_unique_id=largest_photo.file_unique_id,
                            photo_id=largest_photo.file_id, name_user=message.from_user.last_name)
    # Устанавливаем состояние ожидания выбора действия с риском
    await state.set_state(FSMFillForm.fill_input_move)


# Этот хэндлер будет срабатывать, если выбрано действие "Отправка нового риска"
# и переводить в состояние ввода координат риска
@dp.callback_query(StateFilter(FSMFillForm.fill_input_move),
                   Text(text=['new_risk']))
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['enter_new_risk_answer'])
    # Устанавливаем состояние ожидания ввода координат риска
    await state.set_state(FSMFillForm.fill_input_location_risk)


# Этот хэндлер будет срабатывать, если выбрано действие "Устранение риска"
# и переводить в состояние ввода координат риска
@dp.callback_query(StateFilter(FSMFillForm.fill_input_move),
                   Text(text=['elimination_risk']))
async def process_education_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=LEXICON_RU['enter_num_risk_answer'])
    # Устанавливаем состояние ожидания ввода номера риска
    await state.set_state(FSMFillForm.fill_num_risk)


# Этот хэндлер будет срабатывать, если во время выбора действия
# будет введено/отправлено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_input_move))
async def warning_not_gender(message: Message):
    await message.answer(text=LEXICON_RU['text_err_input_move'],
                         reply_markup=new_elimination_risk_kb)


# Этот хэндлер будет срабатывать, если введены корректные координаты
# только из буквенно-цифровых символов и переводить обнулять состояние
@dp.message(StateFilter(FSMFillForm.fill_input_location_risk), F.text)
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "location"
    await state.update_data(location=message.text)
    # Добавляем в "базу данных" фото пользователя и локацию риска
    # по ключу id пользователя
    user_dict[message.from_user.id] = await state.get_data()
    path = f"photo/{(user_dict[message.from_user.id]['location']).replace(' ', '_')}_{user_dict[message.from_user.id]['name_user']}.jpeg"
    await bot.download(user_dict[message.from_user.id]['photo_id'], path)
    await message.answer(text=LEXICON_RU['accepted_review_answer'])
    print(user_dict)
    mail('новый риск', path)
    os.remove(path)
    # Завершаем машину состояний
    await state.clear()


# Этот хэндлер будет срабатывать, если во время ввода координат риска
# будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_input_location_risk))
async def warning_not_name(message: Message):
    await message.answer(text=LEXICON_RU['enter_new_risk_location_err_answer'])


# Этот хэндлер будет срабатывать, если введен корректный номер риска обнулять состояние
@dp.message(StateFilter(FSMFillForm.fill_num_risk), F.text, CorrectInputNumRisk())
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(num_risk=message.text)
    user_dict[message.from_user.id] = await state.get_data()
    path = f"photo/{user_dict[message.from_user.id]['num_risk']}_{user_dict[message.from_user.id]['name_user']}.jpeg"
    await bot.download(user_dict[message.from_user.id]['photo_id'], path)
    await message.answer(text=LEXICON_RU['accepted_review_answer'])
    # Завершаем машину состояний
    print(user_dict)
    mail('устранение риска', path)
    os.remove(path)
    await state.clear()


# Этот хэндлер будет срабатывать, если во время ввода номера риска
# будет введено что-то некорректное
@dp.message(StateFilter(FSMFillForm.fill_num_risk))
async def warning_not_name(message: Message):
    await message.answer(text=LEXICON_RU['enter_elimination_risk_num_err_answer'])


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@dp.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON_RU['other_answer'])


if __name__ == '__main__':
    try:
        # Запускаем polling
        dp.run_polling(bot)

    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        print('Bot stopped!')
