import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from app.database.user import User, UserCollection
from app.states import MainState
from app.keyboards import main_menu
from app.utils import clear_history, append_history, pop_history

router = Router()


@router.message(Command('back'))
async def cmd_back(message: types.Message, state: FSMContext):
    if (
        await state.get_state() is not None
        and (await state.get_data())['state_history']
    ):
        prev_state, handler = await pop_history(state)
        await state.set_state(prev_state)
        await message.answer('{GOING BACK}')
        await handler(message, state)


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


@router.message(MainState.new_user)
async def unknown_handler(message: types.Message):
    await message.answer(
        '{UNKNOWN HANDLER}'
    )

@router.message(MainState.registered_user)
async def registered_user(message: types.Message, state: FSMContext):
    await clear_history(state)
    await message.answer(
        '{REGISTERED USER}',
        reply_markup=ReplyKeyboardRemove()
    )
