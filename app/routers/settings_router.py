import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.user import User, UserCollection
from app.states import MainState, SettingsState
from app.keyboards import main_menu, settings_menu
from app.utils import clear_history, append_history, pop_history

router = Router()


@router.message(MainState.registered_user, Command('settings'))
@router.message(MainState.registered_user, F.text == 'Настройки ⚙️')
async def cmd_settings(message: types.Message, state: FSMContext, command: CommandObject = CommandObject()):
    user = UserCollection.get_user_by_tg_id(
        message.from_user.id,
    )
    settings = user.notification_settings

    await message.answer(
        text='⚙️ Настройки ⚙️',
        reply_markup=settings_menu.get_save()
    )
    await message.answer(
        'Какие уведомления вы хотите получать?',
        reply_markup=settings_menu.get_settings(settings)
    )

    await state.set_state(SettingsState.settings)


@router.message(SettingsState.settings, F.text == 'Сохранить')
async def save(message: types.Message, state: FSMContext):
    await message.answer(
        'Сохраняем ваши настройки!',
        reply_markup=main_menu.get_registered_user()
    )
    await message.answer(
        'Чего вы желаете?',
        reply_markup=main_menu.get_registered_user()
    )
    await state.set_state(MainState.registered_user)


@router.message(SettingsState.settings)
async def save(message: types.Message, state: FSMContext):
    await message.answer(
        'У нас нет такой настройки :(\nНажмите, пожалуйста, на кнопки выше, либо сохраните изменения.'
    )


@router.callback_query(SettingsState.settings, Text("regular_notifications"))
async def flip_reg_notifications(callback: types.CallbackQuery):
    user = UserCollection.get_user_by_tg_id(
        callback.from_user.id,
    )
    settings = user.notification_settings
    settings.regular = not settings.regular

    UserCollection.update_notification_settings_by_tg_id(user.tg_id, user.notification_settings)

    await callback.message.edit_text(
        text='Какие уведомления вы хотите получать?',
        reply_markup=settings_menu.get_settings(settings)
    )


@router.callback_query(SettingsState.settings, Text("events_notifications"))
async def flip_reg_notifications(callback: types.CallbackQuery):
    user = UserCollection.get_user_by_tg_id(
        callback.from_user.id
    )
    settings = user.notification_settings
    settings.events = not settings.events

    UserCollection.update_notification_settings_by_tg_id(user.tg_id, user.notification_settings)

    await callback.message.edit_text(
        text='Какие уведомления вы хотите получать?',
        reply_markup=settings_menu.get_settings(settings)
    )


@router.callback_query(SettingsState.settings, Text("offers_notifications"))
async def flip_reg_notifications(callback: types.CallbackQuery):
    user = UserCollection.get_user_by_tg_id(
        callback.from_user.id
    )
    settings = user.notification_settings
    settings.offers = not settings.offers

    UserCollection.update_notification_settings_by_tg_id(user.tg_id, user.notification_settings)

    await callback.message.edit_text(
        text='Какие уведомления вы хотите получать?',
        reply_markup=settings_menu.get_settings(settings)
    )

