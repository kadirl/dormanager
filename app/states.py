from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    new_user = State()
    registered_user = State()


class RegistrationState(StatesGroup):
    name = State()
    room = State()
