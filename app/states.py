from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    new_user = State()
    registered_user = State()


class RegistrationState(StatesGroup):
    name = State()
    room = State()

class SettingsState(StatesGroup):
    settings = State()


class NotificationState(StatesGroup):
    content = State()


class OfferState(StatesGroup):
    offer = State()
    counter_offer = State()