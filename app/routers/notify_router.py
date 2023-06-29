import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from app.database.user import User, UserCollection
from app.states import MainState, NotificationState
from app.keyboards import main_menu, notify_menu
from app.utils import clear_history, append_history, pop_history
from app import bot

router = Router()


@router.message(Command('notify'))
@router.message(MainState.registered_user, F.text == 'Создать объявление')
async def create_notification(message: types.Message, state: FSMContext):
    await state.set_state(NotificationState.content)
    await message.answer(
        'О чем вы хотите объявить? Ваше сообщения увидят все студенты, у кого включены уведомления от студентов',
        reply_markup=notify_menu.get_cancel()
    )


@router.message(NotificationState.content, F.text == 'Отменить')
async def send_notification(message: types.Message, state: FSMContext):
    await message.answer('Отменяем объявление 👀')
    await state.set_state(MainState.registered_user)
    await clear_history(state)


@router.message(NotificationState.content)
async def send_notification(message: types.Message, state: FSMContext):
    sender = UserCollection.get_user_by_tg_id(message.from_user.id)
    text = f'{sender.name} из комнаты {sender.room} хочет кое-чем со всеми поделиться:\n\n"{message.text}"'

    users = UserCollection.get_regular_notification_allowed_users()

    for user in users:
        if user.tg_id == str(message.from_user.id):
            await message.answer(f'Объявление отправлено успешно!\nЕго получили {len(users)} жителей общежития.')
            await message.answer('Чего вы желаете?', reply_markup=main_menu.get_registered_user())
            continue
        await bot.send_message(user.chat_id, text=text)

    await state.set_state(MainState.registered_user)
    await clear_history(state)

