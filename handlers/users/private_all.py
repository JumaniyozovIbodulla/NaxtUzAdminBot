from aiogram.filters import CommandStart
from aiogram import types, F
from data.loader import dp, router
from data.config import BASE_URL, ADMINS
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from data.loader import bot
from aiogram.enums.chat_action import ChatAction
from keyboards.default.def_keys import welcome_admin, back
from keyboards.inline.inline_buttons import choose_lang
from filters.private import IsPrivate
from aiogram.fsm.context import FSMContext
from utils.misc.language import translate
from utils.misc.db import create_lead_1, create_lead_2, get_lang
from states.user_states import LeadStates

# Start bilan boshlash hamma uchun
@dp.message(CommandStart(), IsPrivate())
async def bot_start_all(message: types.Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    info = message.text.split(" ")[1]
    tarif = info.split("-")[0]
    lang = info.split("-")[1]

    await create_lead_1(message.from_user.id, message.from_user.full_name, message.from_user.username, lang, tarif)
    
    await message.answer(f"{translate["name"][lang]}", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LeadStates.Name)


@router.message(LeadStates.Name)
async def get_name(msg: types.Message, state: FSMContext):
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    await state.update_data({"name": msg.text})
    lang = await get_lang(msg.from_user.id)

    await msg.answer(f"{translate["phone_number"][lang]}", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LeadStates.PhoneNumber)


@router.message(LeadStates.PhoneNumber)
async def get_phone(msg: types.Message, state: FSMContext):
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    await state.update_data({"phone_number": msg.text})
    lang = await get_lang(msg.from_user.id)

    await msg.answer(f"{translate["business_type"][lang]}", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LeadStates.BusinessType)

@router.message(LeadStates.BusinessType)
async def get_phone(msg: types.Message, state: FSMContext):
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    await state.update_data({"business_type": msg.text})
    lang = await get_lang(msg.from_user.id)

    await msg.answer(f"{translate["business_location"][lang]}", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LeadStates.BusinessLocation)



@router.message(LeadStates.BusinessLocation)
async def get_phone(msg: types.Message, state: FSMContext):
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    lang = await get_lang(msg.from_user.id)

    if msg.content_type == "location":
        data = await state.get_data()
        name = data["name"]
        phone_number = data["phone_number"]
        business_type = data["business_type"]

        username = await create_lead_2(msg.from_user.id, name, phone_number, business_type, msg.location.latitude, msg.location.longitude)
        

        text = f"💸 Yangi Lead\n\n👤 Ismi: {name}\n🔗 Username: @{username}\n📞 Raqami: {phone_number}\n🎯 Biznes turi: {business_type}"
        hold = await bot.send_message(ADMINS, text)
        await bot.send_location(ADMINS, msg.location.latitude, msg.location.longitude, reply_to_message_id=hold.message_id)

        
    
        await state.clear()


        await msg.answer(f"{translate["form_completed"][lang]}", reply_markup=ReplyKeyboardRemove())
        return
    

    
    await state.update_data({"business_type": msg.text})
    await msg.answer(f"{translate["business_location"][lang]}", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LeadStates.BusinessLocation)
