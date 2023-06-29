from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    new_user = State()
    learn_more = State()
    registration = State()
    registered_user = State()


class RegistrationState(StatesGroup):
    city = State()
    no_city = State()
    first_name = State()
    last_name = State()
    gender = State()
    email = State()
