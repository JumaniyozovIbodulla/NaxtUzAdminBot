from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton

welcome_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💠 Yangi mijoz qo'shish"),
        ],
        [
            KeyboardButton(text="👀 Mijozlar ma'lumotini olish"),
        ],
        [
            KeyboardButton(text="🎯 QrCode olish"),
        ],
        [
            KeyboardButton(text="🏃‍♂️ Tarifni davom ettirish"),
        ],
        [
            KeyboardButton(text="⚙️ Boshqa tarifga o'tish"),
        ],
        [
            KeyboardButton(text="❌ O'chirish"),
        ]

    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔙 Orqaga qaytish")
        ]
    ],
    resize_keyboard=True
)

