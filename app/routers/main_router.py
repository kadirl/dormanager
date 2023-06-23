from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject


router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message, command: CommandObject):
    await message.answer(str(command.args))
