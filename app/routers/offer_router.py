import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from app.database.user import User, UserCollection
from app.states import MainState, NotificationState, OfferState
from app.keyboards import offer_menu
from app.utils import clear_history, append_history, pop_history
from app import bot

router = Router()


@router.message(Command('offer'))
async def create_notification(message: types.Message, state: FSMContext):
    await state.set_state(OfferState.offer)
    await message.answer('{OFFER REQUEST}')


@router.message(OfferState.offer)
async def send_notification(message: types.Message, state: FSMContext):
    text = message.text
    users = UserCollection.get_offers_notification_allowed_users()

    for user in users:
        if user.tg_id == str(message.from_user.id):
            await bot.send_message('{OFFER SENT}')
        await bot.send_message(user.chat_id, text=text, reply_markup=offer_menu.reply_to_offer())

    await clear_history(state)
