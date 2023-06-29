from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

new_user = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Хочу вступить!')],
        [KeyboardButton(text='Хочу узнать больше')]
    ]
)

registered_user = ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder='fuck me',
    keyboard=[
        [KeyboardButton(text='i am old')]
    ]
)