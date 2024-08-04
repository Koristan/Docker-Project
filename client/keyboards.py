from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder



def create_keyboard(btns):
    kb = [[]]

    for btn in btns:
        kb[0].append(types.KeyboardButton(text=btn),)

    keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True
    )

    return keyboard