import datetime

import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums.parse_mode import ParseMode

from app.database.user import User, UserCollection
from app.database.event import Event, EventsCollection
from app.states import MainState, EventsStat
from app.keyboards import main_menu, notify_menu
from app.filters.events import DateFilter
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
            f'<b>{event.name}</b>\n\n{event.description}\n<b>Время:</b>{event.time}\n<b>Место:</b>{event.place}\n<b>Хост:</b>{host.name}',
            parse_mode=ParseMode.HTML
        )


@router.message(MainState.registered_user, F.text == 'Объявить ивент 🎉')
async def show_events(message: types.Message, state: FSMContext):
    await message.answer(
        'Вау, как круто! Что вы хотите провести? Дайте короткое название вашему мероприятию',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(EventsStat.name)

@router.message(EventsStat.name)
async def show_events(message: types.Message, state: FSMContext):
    await message.answer('Чудесно! А если чуточку подробнее? Дайте описание вашему мероприятию')
    await state.update_data(name=message.text)
    await state.set_state(EventsStat.desc)

@router.message(EventsStat.desc)
async def show_events(message: types.Message, state: FSMContext):
    await message.answer('Уверен, нашим участникам это очень понравится! А стоп, а когда оно будет? Напишите дату проведения мероприятия в формате мм.дд.гг.')
    await state.update_data(description=message.text)
    await state.set_state(EventsStat.date)

@router.message(EventsStat.date, DateFilter())
async def show_events(message: types.Message, state: FSMContext):
    await message.answer('А где оно будет проводиться 🤔? Назовите место проведения мероприятия')
    day, month, year = map(int, message.text.split('.'))
    await state.update_data(time=datetime.datetime(day=day, month=month, year=year+2000))
    await state.set_state(EventsStat.place)

@router.message(EventsStat.date)
async def show_events(message: types.Message, state: FSMContext):
    await message.answer('Неприавильный формат даты. Попробуйте еще раз')

@router.message(EventsStat.place)
async def show_events(message: types.Message, state: FSMContext):
    await message.answer('Все, со всем определились! Сейчас уведомим всех участников 🥰')
    await state.update_data(place=message.text)

    host = UserCollection.get_user_by_tg_id(message.from_user.id)

    data = await state.get_data()
    data['host'] = host.id

    event = Event(**data)
    event_id = EventsCollection.create_event(event)

    users = UserCollection.get_events_notification_allowed_users()

    for user in users:
        if user.tg_id == str(message.from_user.id):
            continue

        await bot.send_message(
            str(user.tg_id),
            f'<b>Объявляем о предстоящем мероприятии!</b>\n<b>{event.name}</b>\n\n{event.description}\n<b>Время:</b>{event.time}\n<b>Место:</b>{event.place}\n<b>Хост:</b>{host.name}',
            parse_mode=ParseMode.HTML
        )

    await state.set_state(MainState.registered_user)
    await message.answer('Чего вы желаете?', reply_markup=main_menu.get_registered_user())