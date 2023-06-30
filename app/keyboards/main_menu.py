from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

BUTTON_NAMES = [
    'Создать объявление 📣', ### DONE
    'Посмотреть ивенты 🎁',### DONE
    'Объявить ивент 🎉',### DONE
    'Предложить обмен 🍽️', ### DONE
    'Оценить соседей 👍👎', ### DONE
    '⚒️ Очередь в прачечной ⚒️',
    'Частые вопросы 🙋', ### DONE
    'Настройки ⚙️' ### DONE
]


def get_new_user():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Давай!')]
        ]
    )


def get_registered_user():
    builder = ReplyKeyboardBuilder()

    for button in BUTTON_NAMES:
        builder.button(text=button)

    builder.adjust(2)

    return builder.as_markup()
