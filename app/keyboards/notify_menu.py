from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from app.database.user import UserNotifications


def get_cancel():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(
            text='Отменить'
        )]
    ])

