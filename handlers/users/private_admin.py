from aiogram.filters import CommandStart
from aiogram import types, F
from data.loader import dp, router
from data.config import BASE_URL
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from utils.misc.helpers import is_valid_uuid
from data.loader import bot
from states.user_states import UserStates
from aiogram.fsm.context import FSMContext
from aiogram.enums.chat_action import ChatAction
from keyboards.default.def_keys import welcome_admin, back
from keyboards.inline.inline_buttons import option
from requests import patch
from datetime import datetime
import pytz
from aiogram.types import BufferedInputFile
from .utilities import generate_modern_qr_pdf

# Tashkent timezone
tz = pytz.timezone("Asia/Tashkent")


VERSION = "/api/v1/"


# Get CR Code
@dp.message(F.text == "🎯 QrCode olish")
async def gen_qr_code(msg: types.Message, state: FSMContext):
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    await msg.answer("✒️ Linkni yuboring",reply_markup=back)
    await state.set_state(UserStates.GenerateQrCode)

@router.message(UserStates.GenerateQrCode)
async def gen_qr_code_2(msg: types.Message, state: FSMContext):
    await bot.send_chat_action(msg.chat.id, ChatAction.UPLOAD_DOCUMENT)

    # PDF yaratish
    pdf_path = await generate_modern_qr_pdf(msg.text)

    # Faylni o'qish
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    pdf_file = BufferedInputFile(pdf_bytes, filename="qr_code.pdf")


    await msg.answer_document(pdf_file, reply_markup=welcome_admin, caption=f"Pdf fayl tayyor ✅")

    await state.clear()

# back to main
@dp.message(F.text == "🔙 Orqaga qaytish")
async def back_to_admin(msg: types.Message, state: FSMContext):
    await state.clear()
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    await msg.answer("Qaytganingizdan xursandman 😊", reply_markup=welcome_admin)



# Start bilan boshlash faqat admin uchun
@dp.message(CommandStart())
async def handle_start(message: types.Message):
    if message.chat.type == "private" and message.from_user.id == 1109659429:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        await message.answer("👀 Quyidagilardan birortasini tanlang:", reply_markup=welcome_admin)



# New Client add
@dp.message(F.text == "💠 Yangi mijoz qo'shish")
async def add_new_client(msg: types.Message, state: FSMContext):
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    await msg.answer("👤 Ismini kiriting:",reply_markup=back)
    await state.set_state(UserStates.client)

@router.message(UserStates.client)
async def add_new_client_phone(msg: types.Message, state: FSMContext):
    if len(msg.text) > 3:
        await state.set_state(UserStates.phone)
        await state.set_data({"name": msg.text})
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("📞 Telefon raqamni kiriting:(99 686 03 07)", reply_markup=back)

    else:
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("❗️Iltimos to'g'ri <b>ism</b>ni kiriting:", reply_markup=back)



@router.message(UserStates.phone)
async def add_new_cost(msg: types.Message, state: FSMContext):
    if len(msg.text) > 11:
        await state.set_state(UserStates.cost)
        await state.set_data({"phone": msg.text})
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("💸 Narxni kiriting:(300000)", reply_markup=back)

    else:
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("❗️Iltimos to'g'ri <b>raqamni</b>ni kiriting:", reply_markup=back)


@router.message(UserStates.cost)
async def add_tariff(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        await state.set_state(UserStates.tariff)
        await state.set_data({"cost": msg.text})
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("👁‍🗨 Tarifni tanlang:(<code>Standard</code> | <code>Premium</code> | <code>Enterprise</code>)", reply_markup=back)

    else:
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("❗️Iltimos to'g'ri <b>narx</b>ni kiriting:", reply_markup=back)


@router.message(UserStates.tariff)
async def add_branch(msg: types.Message, state: FSMContext):
    if msg.text in ["Standard", "Premium", "Enterprise"]:
        await state.set_state(UserStates.count_of_branches)
        await state.set_data({"tariff": msg.text})
        if msg.text == "Standard":
            await state.set_data({"tariff_limit": "1000"})
        
        elif msg.text == "Premium":
            await state.set_data({"tariff_limit": "5000"})

        elif msg.text == "Enterprise":
            await state.set_data({"tariff_limit": "10000"})

        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("✒️ Filiallar sonini kiriting:", reply_markup=back)

    else:
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("❗️Iltimos to'g'ri <b>tarif</b>ni kiriting:", reply_markup=back)



@router.message(UserStates.count_of_branches)
async def add_billing_cycle(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        await state.set_state(UserStates.verify)
        await state.set_data({"count_of_branches": msg.text})
      
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("👀 To'lov muddatini tanlang:(<code>Monthly</code> | <code>Annually</code>)", reply_markup=back)

    else:
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("❗️Iltimos to'g'ri <b>son</b>ni kiriting:", reply_markup=back)



@router.message(UserStates.verify)
async def verify_all(msg: types.Message, state: FSMContext):
    if msg.text in ["Monthly", "Annually"]:
        await state.set_data({"billing_cycle": msg.text})
        
        data = await state.get_data()
        print(f"\n\ndata: {data}\n")
        name = data["name"]
        phone = data["phone"]
        cost = data["cost"]
        tariff = data["tariff"]
        tariff_limit = data["tariff_limit"]
        count_of_branches = data["count_of_branches"]


        # time
        now = datetime.now(tz)
        now_str = now.isoformat()


        text = f"""👤 Ism: {name}
📞 Telefon raqam: {phone}
💶 Summa: {cost} so'm
🐵 Tarif: {tariff}
🔗 Tarif limit: {tariff_limit} tagacha
🔢 Filiallar soni: {count_of_branches} ta

⏳ Qo'shilish vaqti: {now_str}

🟢 Tasdiqlaysizmi?
"""
        

        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer(text, reply_markup=option)



    #     url = BASE_URL + VERSION + "order-coordinates"

    #     headers = {
    #     "Content-Type": "application/json",
    #     }

    #     req = {
    #         "id": id,
    #         "lat": lat,
    #         "long": long
    #     }

    #     response = patch(url, json=req, headers=headers)

    #     print(f"ID: {id}\nStatus code: {response.status_code}")

    #     if response.status_code == 200:
    #         await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    #         await msg.answer("Buyurtmaga lakatsiya muvaffaqiyatli biriktirildi ✅", reply_markup=welcome_admin)
    #     else:
    #         await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    #         await msg.answer("😥 Xatolik bo'ldi birozdan so'ng urinib ko'ring", reply_markup=welcome_admin)


    else:
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("❗️Iltimos faqat <b>tarif muddatini</b> qayta yuboring", reply_markup=back)



# Complaints
@dp.message(F.text == "🎯 Shikoyatga lakatsiya biriktirish")
async def give_to_complaint_1(msg: types.Message, state: FSMContext):
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    await msg.answer("🆔 Shikoyatning IDsini yuboring:",reply_markup=back)
    await state.set_state(UserStates.complaint)

@router.message(UserStates.complaint)
async def give_to_complaint_2(msg: types.Message, state: FSMContext):
    if await is_valid_uuid(msg.text):
        await state.set_state(UserStates.complaint_location)
        await state.set_data({"id": msg.text})
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("📍 Lokatsiyani yuboring:", reply_markup=back)

    else:
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("❗️Iltimos to'g'ri <b>ID</b>ni kiriting:", reply_markup=back)

@router.message(UserStates.complaint_location)
async def give_to_complaint_3(msg: types.Message, state: FSMContext):
    if msg.content_type == "location":
        data = await state.get_data()
        id = data["id"]
        lat = msg.location.latitude
        long = msg.location.longitude

        url = BASE_URL + VERSION + "complaint-coordinates"

        headers = {
        "Content-Type": "application/json",
        }

        req = {
            "id": id,
            "lat": lat,
            "long": long
        }

        response = patch(url, json=req, headers=headers)

        print(f"ID: {id}\nStatus code: {response.status_code}")

        if response.status_code == 200:
            await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
            await msg.answer("Shikoyatga lakatsiya muvaffaqiyatli biriktirildi ✅", reply_markup=welcome_admin)
        else:
            await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
            await msg.answer("😥 Xatolik bo'ldi birozdan so'ng urinib ko'ring", reply_markup=welcome_admin)

        await state.clear()

    else:
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("❗️Iltimos faqat <b>lokatsiyani</b> yuboring", reply_markup=back)




# Clients
@dp.message(F.text == "🏬 Mijozga lakatsiya biriktirish")
async def give_to_client_1(msg: types.Message, state: FSMContext):
    await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
    await msg.answer("🆔 Mijozning IDsini yuboring:",reply_markup=back)
    await state.set_state(UserStates.client)

@router.message(UserStates.client)
async def give_to_client_2(msg: types.Message, state: FSMContext):
    if await is_valid_uuid(msg.text):
        await state.set_state(UserStates.client_location)
        await state.set_data({"id": msg.text})
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("📍 Lokatsiyani yuboring:", reply_markup=back)

    else:
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("❗️Iltimos to'g'ri <b>ID</b>ni kiriting:", reply_markup=back)

@router.message(UserStates.client_location)
async def give_to_client_3(msg: types.Message, state: FSMContext):
    if msg.content_type == "location":
        data = await state.get_data()
        id = data["id"]
        lat = msg.location.latitude
        long = msg.location.longitude

        url = BASE_URL + VERSION + "client-coordinates"

        headers = {
        "Content-Type": "application/json",
        }

        req = {
            "id": id,
            "lat": lat,
            "long": long
        }

        response = patch(url, json=req, headers=headers)

        print(f"ID: {id}\nStatus code: {response.status_code}")

        if response.status_code == 200:
            await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
            await msg.answer("Mijozga lakatsiya muvaffaqiyatli biriktirildi ✅", reply_markup=welcome_admin)
        else:
            await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
            await msg.answer("😥 Xatolik bo'ldi birozdan so'ng urinib ko'ring", reply_markup=welcome_admin)

        await state.clear()

    else:
        await bot.send_chat_action(msg.chat.id, ChatAction.TYPING)
        await msg.answer("❗️Iltimos faqat <b>lokatsiyani</b> yuboring", reply_markup=back)

