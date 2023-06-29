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


@router.message(Command('notification'))
async def create_notification(message: types.Message, state: FSMContext):
    await state.set_state(NotificationState.content)

@router.message(NotificationState.content)
async def send_notification(message: types.Message, state: FSMContext):
    text = message.text


    users = UserCollection.get_regular_notification_allowed_users()
    for user in users:
        await bot.send_message(user.tg_id, text='text')

    await clear_history(state)


@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext, command: CommandObject = CommandObject()):
    await clear_history(state)

    id = command.args
    user = None

    if bson.ObjectId.is_valid(id):
        user = UserCollection.get_user_by_id(id)

    if user is None:
        await append_history(cmd_start, state)
        await state.set_state(MainState.new_user)
        await message.answer(
            'Привет, я бот общежития nFactorial! 👋\nНе желаете представиться?',
            reply_markup=main_menu.new_user
        )
    else:
        await state.set_state(MainState.registered_user)
        await message.answer(
            f'Привет, {user.name}! 👋\n Чего желаете?',
            reply_markup=main_menu.registered_user
        )

