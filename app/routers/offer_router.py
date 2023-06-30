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
    await message.answer(
        text='Чего вы хотите и что можете предложить взамен? 🤔',
        reply_markup=offer_menu.get_cancel()
    )


@router.message(OfferState.offer, F.text == 'Отменить')
async def send_offer(message: types.Message, state: FSMContext):
    await state.set_state(MainState.registered_user)
    await message.answer('Чего вы желаете?', reply_markup=main_menu.get_registered_user())


@router.message(OfferState.offer)
async def send_offer(message: types.Message, state: FSMContext):
    text = message.text
    users = UserCollection.get_offers_notification_allowed_users()
    myself = UserCollection.get_user_by_tg_id(message.from_user.id)

    offer_id = OfferCollection.create_offer(
        Offer(
            issuer_id=UserCollection.get_user_by_tg_id(message.from_user.id).id,
            text=text
        )
    )
    print(offer_id)

    for user in users:
        if user.tg_id == str(message.from_user.id):
            await message.answer('Ваш обмен отправлен другим постояльцам общежития :)\nВ скором времени, вам должны будут ответить ваши любимые соседи ❤️')
            continue
        await bot.send_message(
            chat_id=user.chat_id,
            text=f'{myself.name} из комнаты {myself.room} предлагает:\n\n"{text}"',
            reply_markup=offer_menu.reply_to_offer(offer_id))

    await state.set_state(MainState.registered_user)
    await message.answer('Чего вы желаете?', reply_markup=main_menu.get_registered_user())




@router.callback_query(Text(startswith="interested"))
async def counter_offer(callback: types.CallbackQuery, state: FSMContext):
    asking_user = UserCollection.get_user_by_tg_id(callback.from_user.id)
    print(asking_user)

    offer = OfferCollection.get_offer_by_id(callback.data.split(':')[1])
    print(offer)

    issuer_user = UserCollection.get_user_by_id(offer.issuer_id)
    print(issuer_user)

    await callback.message.answer(
        text=f'Вы можете связаться с {issuer_user.name} нажав на кнопку ниже"',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='Свяазаться',
                url=f't.me/{issuer_user.username}'
            )]
        ])
    )

    await bot.send_message(
        issuer_user.tg_id,
        text=f'{asking_user.name} заинтересован в вашем предложении обмена:\n\n"{offer.text}"',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='Свяазаться',
                url=f't.me/{callback.from_user.username}'
            )]
        ])
    )
