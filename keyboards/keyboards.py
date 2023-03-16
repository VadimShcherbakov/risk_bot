from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from lexicon.lexicon_ru import LEXICON_RU

# Создаем объекты инлайн-кнопок
new_risk_button = InlineKeyboardButton(text=LEXICON_RU['new_risk_button'],
                                       callback_data='new_risk')
elimination_risk_button = InlineKeyboardButton(text=LEXICON_RU['elimination_risk_button'],
                                               callback_data='elimination_risk')

# Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
keyboard: list[list[InlineKeyboardButton]] = [[new_risk_button, elimination_risk_button]]
# Создаем объект инлайн-клавиатуры
new_elimination_risk_kb = InlineKeyboardMarkup(inline_keyboard=keyboard)

