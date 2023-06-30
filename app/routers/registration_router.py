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
    await message.answer('Как вас зовут? Напишите, пожалуйста, ваше имя и фамилию кириллицей', reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.name)


@router.message(RegistrationState.name, NameFilter())
async def name_handler(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(f'Приятно познакомиться, {name}! В какой комнате вы живете?')
    await state.set_state(RegistrationState.room)


@router.message(RegistrationState.name)
async def invalid_name(message: types.Message, state: FSMContext):
    await message.answer('Извините, но такое имя у нас нельзя :(\nНапишите еще раз')


@router.message(RegistrationState.room, RoomFilter())
async def room_handler(message: types.Message, state: FSMContext):
    room = int(message.text)
    await state.update_data(room=room)
    await message.answer(f'Юху! Мы закончили нашу коротенькую регистрацию. Теперь вы член нашей семьи!', reply_markup=main_menu.get_registered_user())
    await state.set_state(MainState.registered_user)

    await state.update_data(tg_id=message.from_user.id)
    await state.update_data(chat_id=message.chat.id)
    await state.update_data(username=message.from_user.username)

    UserCollection.create_user(
        User(
            **(await state.get_data())
        )
    )

    await clear_history(state)


@router.message(RegistrationState.room)
async def invalid_room_handler(message: types.Message, state: FSMContext):
    await message.answer('Номером комтаны может быть любое целое число от 1 до 200. У вас оно, кажется, не такое. Попробуйте еще раз :)')
