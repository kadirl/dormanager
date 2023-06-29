import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from app.states import MainState, RegistrationState
from app.keyboards import registration, main_menu
from app.database import database
from app.filters.registration import FirstLastNameFilter, EmailFilter
from app.utils import pop_history, append_history, clear_history


router = Router()

# @router.message(Command('reg'))
# @router.message(MainState.new_user, F.text == 'Хочу вступить!')
# async def reg_start_handler(message: types.Message, state: FSMContext):
#     await message.answer('{CITY REQUEST}?', reply_markup=registration.get_cities(country='kazakhstan'))
#     await state.set_state(RegistrationState.city)


# @router.message(RegistrationState.city, F.text == '{NO CITY}')
# async def no_city_handler(message: types.Message, state: FSMContext):
#     await message.answer(
#         '{NO CITY TEXT}',
#         reply_markup=registration.get_position_form_link()
#     )
#
#
# @router.message(
#     RegistrationState.city,
#     F.text.lower().in_([
#         city.name
#         for city
#         in CountryCollection.get_cities_by_country('kazakhstan')
#     ])
# )
# async def no_city_handler(message: types.Message, state: FSMContext):
#     await message.answer(
#         f'{message.text} NAME REQUEST',
#         reply_markup=ReplyKeyboardRemove()
#     )
#     await state.update_data(city=message.text)
#     await state.set_state(RegistrationState.first_name)
#
#
# @router.message(RegistrationState.city)
# async def invalid_city_handler(message: types.Message, state: FSMContext):
#     await message.answer(
#         '{INVALID CITY NAME TRY AGAIN OR BECOME CORD}',
#         reply_markup=registration.get_position_form_link()
#     )
#
#
# @router.message(RegistrationState.first_name, FirstLastNameFilter())
# async def first_name_handler(message: types.Message, state: FSMContext):
#     name = message.text
#     await state.update_data(first_name=name)
#     await message.answer(f'{name} LAST NAME REQUEST')
#     await state.set_state(RegistrationState.last_name)
#
#
# @router.message(RegistrationState.last_name, FirstLastNameFilter())
# async def last_name_handler(message: types.Message, state: FSMContext):
#     name = message.text
#     await state.update_data(last_name=name)
#     await message.answer(f'GENDER REQUEST', reply_markup=registration.get_gender())
#     await state.set_state(RegistrationState.gender)
#
#
# @router.message(
#     StateFilter(RegistrationState.last_name, RegistrationState.first_name)
# )
# async def invalid_first_or_last_name(message: types.Message, state: FSMContext):
#     await message.answer('Invalid first or last name. Try again')
#
#
# @router.message(RegistrationState.gender, F.text.in_(['male', 'female']))
# async def gender_handler(message: types.Message, state: FSMContext):
#     gender = message.text
#     await state.update_data(gender=gender)
#     await message.answer(f'We are almost done! What is your email?', reply_markup=ReplyKeyboardRemove())
#     await state.set_state(RegistrationState.email)
#
#
# @router.message(RegistrationState.gender)
# async def invalid_gender(message: types.Message, state: FSMContext):
#     await message.answer(f'Invalid gender. Choose the one from buttons below')
#
#
#

#
#

#
#

#
#
# @router.message(RegistrationState.email, EmailFilter)
# async def email(message: types.Message, state: FSMContext):
#     email = message.text
#     await state.update_data(email=email)
#
#     await message.answer('Great! ')
#
#
# @router.message(RegistrationState.email)
# async def invalid_email(message: types.Message, state: FSMContext):
#     await message.answer(f'Invalid email. Try again')
