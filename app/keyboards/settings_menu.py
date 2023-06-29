from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from app.database.user import UserNotifications


def _get_emoji(status):
    return "✅" if status else "❌"


def get_settings(settings: UserNotifications):

    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f'Оповещения от студентов: {_get_emoji(settings.regular)}',
            callback_data='regular_notifications'
        )],
        [InlineKeyboardButton(
            text=f'Оповещения об офферах: {_get_emoji(settings.offers)}',
            callback_data='offers_notifications'
        )],
        [InlineKeyboardButton(
            text=f'Оповещения об ивентах: {_get_emoji(settings.events)}',
            callback_data='events_notifications'
        )],
    ])

def get_save():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(
            text='Сохранить'
        )]
    ])

