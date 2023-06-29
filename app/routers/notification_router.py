import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from app.database.user import User, UserCollection
from app.states import MainState, NotificationState
from app.keyboards import main_menu
from app.utils import clear_history, append_history, pop_history
from app import bot

router = Router()


@router.message(Command('notify'))
@router.message(MainState.registered_user, F.text == '{NOTIFY}')
async def create_notification(message: types.Message, state: FSMContext):
    await state.set_state(NotificationState.content)
    await message.answer('{NOTIFICATION REQUEST}')


@router.message(NotificationState.content)
async def send_notification(message: types.Message, state: FSMContext):
    text = message.text
    users = UserCollection.get_regular_notification_allowed_users()

    for user in users:
        if user.tg_id == str(message.from_user.id):
            await bot.send_message('{NOTIFICATION SENT}')
        await bot.send_message(user.chat_id, text=text)

    await state.set_state(MainState.registered_user)
    await clear_history(state)

