from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


choose_lang = InlineKeyboardMarkup(inline_keyboard=[
    [
            InlineKeyboardButton(
                text="🇺🇿 Lotincha",
                callback_data = "language_uz"
            ),

             InlineKeyboardButton(
                text="🇺🇸 English",
                callback_data = "language_en"
            ),

            InlineKeyboardButton(
                text="🇷🇺 Русский язык",
                callback_data = "language_ru"
            )
        ]
    ]
)



option = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🫡 Ha",
                    callback_data="yes"
                ),

                InlineKeyboardButton(
                    text="🚫 Yo'q",
                    callback_data="no"
                )
            ]
        ])
