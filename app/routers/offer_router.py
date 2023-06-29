import bson
from aiogram import Router, types, F
from aiogram.filters import Text
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from app.database.user import User, UserCollection
from app.database.offers import Offer, OfferCollection
from app.states import MainState, NotificationState, OfferState
from app.keyboards import offer_menu, main_menu
from app.utils import clear_history, append_history, pop_history
from app import bot

router = Router()


@router.message(Command('offer'))
@router.message(MainState.registered_user, F.text == 'Предложить обмен 🍽️')
async def create_offer(message: types.Message, state: FSMContext):
    await state.set_state(OfferState.offer)
    await message.answer(text='Чего вы хотите и что можете предложить взамен? 🤔')


@router.message(OfferState.offer)
async def send_offer(message: types.Message, state: FSMContext):
    text = message.text
    users = UserCollection.get_offers_notification_allowed_users()

    for user in users:
        if user.tg_id == str(message.from_user.id):
            await message.answer('Ваш обмен отправлен другим постояльцам общежития :)\nВ скором времени, вам должны будут ответить ваши любимые соседи ❤️')
        await bot.send_message(chat_id=user.chat_id, text=text, reply_markup=offer_menu.reply_to_offer())

    await state.set_state(MainState.registered_user)
    await message.answer('Чего вы желаете?', reply_markup=main_menu.get_registered_user())

    OfferCollection.create_offer(
        Offer(
            issuer_id=UserCollection.get_user_by_tg_id(message.from_user.id)._id,
            text=text
        )
    )


@router.callback_query(Text("counter_offer"))
async def counter_offer(callback: types.CallbackQuery, state: FSMContext):
    user = UserCollection.get_user_by_tg_id(callback.from_user.id)
    offer = OfferCollection.get_offer_by_issuer_id(user._id)

    await state.set_state(OfferState.counter_offer)
    await callback.message.answer(
        text=f'{user.name} заинтересован  вам следующее по '
    )


# @router.message(OfferState.counter_offer)
# async def send_counter_offer(message: types.Message, state: FSMContext):
#     text = message.text
#     chat_id_of_offer_sender = 529158582
#     await bot.send_message(chat_id=chat_id_of_offer_sender, text=text, reply_markup=offer_menu.reply_to_counter_offer())
#

# @router.callback_query(Text("another_offer"))
# async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
#     await state.set_state(OfferState.offer)
#     await callback.message.answer(text='{OFFER REQUEST}')