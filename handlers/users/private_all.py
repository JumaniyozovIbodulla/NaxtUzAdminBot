from aiogram.filters import CommandStart
from aiogram import types, F
from data.loader import dp, router
from data.config import BASE_URL
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from data.loader import bot
from aiogram.enums.chat_action import ChatAction
from keyboards.default.def_keys import welcome_admin, back
from keyboards.inline.inline_buttons import choose_lang
from filters.private import IsPrivate
from aiogram.fsm.context import FSMContext



# Start bilan boshlash hamma uchun
@dp.message(CommandStart(), IsPrivate())
async def bot_start_all(message: types.Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    message_hold = await message.answer(f"""🎯 Tilni tanlang:
🎯 Тилни танланг:
🎯 Выберите язык:""", reply_markup=choose_lang)
