import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from app.states import MainState, RatingState
from app.keyboards import main_menu
from app.database.user import User, UserCollection
from app.filters.registration import NameFilter, RoomFilter
from app.utils import pop_history, append_history, clear_history


router = Router()


@router.message(Command('rate'))
async def number_handler(message: types.Message, state: FSMContext):
    await message.answer('Enter room number')
    await state.set_state(RatingState.number)


@router.message(RatingState.number)
async def name_handler(message: types.Message, state: FSMContext):
    number = int(message.text)
    await state.update_data(number=number)
    await message.answer('Success')
    await message.answer('Rate room')
    await state.set_state(RatingState.rate)


# @router.message(RegistrationState.name)
# async def invalid_name(message: types.Message, state: FSMContext):
#     await message.answer('{INVALID NAME}')



@router.message(RatingState.rate)
async def rate_handler(message: types.Message, state: FSMContext):
    rate = int(message.text)
    await state.update_data(rate=rate)
    await message.answer('Success')
    await message.answer('Напишите отзыв')
    await state.set_state(RatingState.text)


@router.message(RatingState.text)
async def text_handler(message: types.Message, state: FSMContext):
    text = message.text
    sender = UserCollection.get_user_by_tg_id(message.from_user.id)
    await message.answer('Success')
    await state.set_state(MainState.registered_user)
    await clear_history(state)
    await message.answer('Чего вы желаете?', reply_markup=main_menu.get_registered_user())

# @router.message(RegistrationState.room)
# async def invalid_room_handler(message: types.Message, state: FSMContext):
#     await message.answer('{INVALID ROOM}')
