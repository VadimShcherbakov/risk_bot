from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------

# Создаем кнопки с ответами согласия и отказа
button_new_risk: KeyboardButton = KeyboardButton(text=LEXICON_RU['new_risk_button'])
button_elimination_risk: KeyboardButton = KeyboardButton(text=LEXICON_RU['elimination_risk_button'])

# Инициализируем билдер для клавиатуры с кнопками "Отправка нового риска" и "Устранение риска"
yes_no_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=2
yes_no_kb_builder.row(button_new_risk, button_elimination_risk, width=2)

# Создаем клавиатуру с кнопками "Отправка нового риска" и "Устранение риска"
new_elimination_risk_kb = yes_no_kb_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)

