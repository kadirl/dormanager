import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from app.states import MainState, RegistrationState
from app.keyboards import main_menu
from app.database.user import User, UserCollection
from app.filters.registration import NameFilter, RoomFilter
from app.utils import pop_history, append_history, clear_history


router = Router()

@router.message(Command('reg'))
@router.message(MainState.new_user, F.text == 'Давай!')
async def reg_start_handler(message: types.Message, state: FSMContext):
    await message.answer('{NAME REQUEST}?', reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.name)


@router.message(RegistrationState.name, NameFilter())
async def name_handler(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(f'{name} ENTER ROOM')
    await state.set_state(RegistrationState.room)


@router.message(RegistrationState.name)
async def invalid_name(message: types.Message, state: FSMContext):
    await message.answer('{INVALID NAME}')


@router.message(RegistrationState.room, RoomFilter())
async def room_handler(message: types.Message, state: FSMContext):
    room = int(message.text)
    await state.update_data(room=room)
    await message.answer(message.text + '{ROOM COMPLETE}', reply_markup=main_menu.get_registered_user())
    await state.set_state(MainState.registered_user)
    await clear_history(state)

    await state.update_data(tg_id=message.from_user.id)
    await state.update_data(chat_id=message.chat.id)


    UserCollection.create_user(
        User(
            **(await state.get_data())
        )
    )


@router.message(RegistrationState.room)
async def invalid_room_handler(message: types.Message, state: FSMContext):
    await message.answer('{INVALID ROOM}')
