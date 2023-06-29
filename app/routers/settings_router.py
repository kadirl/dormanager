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


# @router.message(MainState.registered_user, Command('settings'))
# @router.message(MainState.registered_user, F.text == '{SETTINGS}')
# async def cmd_settings(message: types.Message, state: FSMContext, command: CommandObject = CommandObject()):
#     await append_history(state)
#
#     id = message.from_user.id
#     print(id)
#     user = UserCollection.get_user_by_tg_id(id)
#
#     if user is None:
#         await append_history(cmd_start, state)
#         await state.set_state(MainState.new_user)
#         await message.answer(
#             'Привет, я бот общежития nFactorial! 👋\nНе желаете представиться?',
#             reply_markup=main_menu.get_new_user()
#         )
#     else:
#         await state.set_state(MainState.registered_user)
#         await message.answer(
#             f'Привет, {user.name}! 👋\n Чего желаете?',
#             reply_markup=main_menu.get_registered_user()
#         )
#


