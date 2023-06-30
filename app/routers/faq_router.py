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


text = '''Q: Где находится общежитие? 
А: ул. Габдулина 2

Q: Каковы условия проживания в общежитии?
A: В вашей уютной комнате у вас будет стол, табуретка и кровать на каждого из ваших соседей, коих у вас может быть до 4, а в добавок – приятный бонус в виде семьи самых дружелюбных древесных клопов :) 

Q: Можно ли будет в общежитии готовить? 
A: Да, конечно, на каждом этаже есть по две кухни, с холодильниками, но будьте бдительным, потому что в наших магических холодильниках иногда исчезает молоко

Q: Где можно покушать, если не хочется готовить? 
A: Рядом есть самая лучшая столовая на свете – тамак. Неподалеку от нее есть еще унихаб, но не такой крутой. А еще, вы можете украсть еду у своего сокамерника соседа, пока он спит, но лучше не этом не попадаться :)

Q: А что насчет развлечений? 
A: Каких развлечений? Проекты делать нужно. Времени у вас будет только на “увлекательный мир одиночного кодинга своего приложения” (с) Далида

Q: Какие принадлежности нужно взять с собой? 
A: Хорошее настроение, желание работать над собой и своим проектом, а также ноутбук, зарядку к нему, конфетки для вахтерш и дихлофос от противных соседей 🤩'''


@router.message(MainState.registered_user, F.text == 'Частые вопросы 🙋')
async def show_events(message: types.Message, state: FSMContext):
    await message.answer(text)
