import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums.parse_mode import ParseMode

from app.database.user import User, UserCollection
from app.database.event import Event, EventsCollection
from app.states import MainState, NotificationState
from app.keyboards import main_menu, notify_menu
from app.utils import clear_history, append_history, pop_history
from app import bot

router = Router()


@router.message(MainState.registered_user, F.text == 'Посмотреть ивенты 🎁')
async def show_events(message: types.Message, state: FSMContext):
    await message.answer('В скором времени у нас ожидаются следующие мероприятия:')

    events = EventsCollection.get_upcoming_events()
    for event in events:
        host = UserCollection.get_user_by_id(event.host)

        await message.answer(
            f'<b>{event.name}</b>\n{event.description}\nВремя:{event.time}\nМесто:{event.place}\nХост:{host.name}',
            parse_mode=ParseMode.HTML
        )

