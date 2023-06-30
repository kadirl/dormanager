import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from app import bot
from app.states import MainState, RatingState
from app.keyboards import main_menu
from app.database.user import User, UserCollection
from app.database.room import RoomCollection, RoomRating, Room
from app.filters.rating import RoomFilter, RateFilter
from app.utils import pop_history, append_history, clear_history

router = Router()


@router.message(Command('rate'))
@router.message(MainState.registered_user, F.text == 'Оценить соседей 👍👎')
async def number_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите номер комнаты')
    await state.set_state(RatingState.number)


@router.message(RatingState.number, RoomFilter())
async def name_handler(message: types.Message, state: FSMContext):
    number = int(message.text)
    await state.update_data(number=number)
    await message.answer('Дайте оценку комнате')
    await state.set_state(RatingState.rate)


@router.message(RatingState.number)
async def invalid_name(message: types.Message, state: FSMContext):
    await message.answer('Неправильный номер комнаты')


@router.message(RatingState.rate, RateFilter())
async def rate_handler(message: types.Message, state: FSMContext):
    rate = int(message.text)
    await state.update_data(rate=rate)
    await message.answer('Напишите отзыв')
    await state.set_state(RatingState.text)


@router.message(RatingState.rate)
async def invalid_name(message: types.Message, state: FSMContext):
    await message.answer('Рейтинг должен быть от 1 до 5')


@router.message(RatingState.text)
async def text_handler(message: types.Message, state: FSMContext):
    text = message.text
    sender = UserCollection.get_user_by_tg_id(message.from_user.id)
    data = (await state.get_data())
    await message.answer('Ваш отзыв сохранен')

    if RoomCollection.get_room_by_number(data['number']) is None:
        RoomCollection.create_room(
            Room(
                number=data['number'],
            )
        )

    RoomCollection.add_room_rating(
        data['number'],
        RoomRating(
            rating=data['rate'],
            text=text,
            sender_id=sender.id
        )
    )

    # функция которая предупреждает о новом отзыве
    users = UserCollection.get_users_by_room_number(data['number'])
    final_res = f"<b>У вашей комнаты новый отзыв:</b>\n'{text}'\n{str(data['rate'])}/5"
    for user in users:
        await bot.send_message(chat_id=user.chat_id, text=final_res, parse_mode="HTML")

    await state.set_state(MainState.registered_user)
    await clear_history(state)
    await message.answer('Чего вы желаете?', reply_markup=main_menu.get_registered_user())


@router.message(Command('rating'))
async def list_rating_handler(message: types.Message, state: FSMContext):
    rooms = RoomCollection.get_all_rooms()
    rating = ''
    for count, room in enumerate(rooms):
        if count+1 == 1:
            rating += '🥇' + 'Комната №' + str(room.number) + ': ' + str(round(room.rating, 1)) + '/5.0\n'
        elif count+1 == 2:
            rating += '🥈' + 'Комната №' + str(room.number) + ': ' + str(round(room.rating, 1)) + '/5.0\n'
        elif count + 1 == 3:
            rating += '🥉' + 'Комната №' + str(room.number) + ': ' + str(round(room.rating, 1)) + '/5.0\n'
        else:
            rating += str(count+1) + '.' + 'Комната №' + str(room.number) + ': ' + str(round(room.rating, 1)) + '/5.0\n'

    await message.answer(rating)
    await state.set_state(MainState.registered_user)
    await clear_history(state)

@router.message(Command('get_my_ratings'))
async def get_ratings_handler(message: types.Message, state: FSMContext):
    room_number = UserCollection.get_user_by_tg_id(message.from_user.id).room
    rooms = RoomCollection.get_room_by_number(room_number)
    final_res = ''

    for counter, room in enumerate(rooms.ratings):
        final_res += str(counter+1) + '. ' + str(room.rating) + '/5\n' + room.text + '\n\n'

    await message.answer(final_res)
    await state.set_state(MainState.registered_user)
    await clear_history(state)

