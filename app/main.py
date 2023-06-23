from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command

# async def show_states(user_id):
#     state = dp.current_state(user=user_id)
#     user_data = await state.get_data()
#     print('Data:', user_data)
#     user_state = await state.get_state()
#     print('State:', user_state)

class MainState(StatesGroup):
    start = State()
    registration = State()

class Registration(StatesGroup):
    name = State()  # Will be represented as 'Registration:name'
    email = State()  # Will be represented as 'Registration:email'

bot = Bot(token='BOT TOKEN')
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands='start', state='*')
async def cmd_start(message: types.Message, command: Command.CommandObj):
    print('cmd start')
    print(command.args)
    await MainState.start.set()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
