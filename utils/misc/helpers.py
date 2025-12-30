from aiogram import Bot
from data.config import ADMINS
import uuid

async def start_bot(bot: Bot) -> None:
    """
    This function is notify to admins about bot is working
    """

    try:
        await bot.send_message(chat_id=ADMINS, text="Bot is working ✅")
        
    except:
            
        raise Exception("Chat not found")

async def stop_bot(bot: Bot):
    """
    This function is notify to admins about bot is stopped
    """

    for admin in ADMINS:

        try:
            await bot.send_message(chat_id=admin, text="Bot is stopped 🛑")
        
        except:

            raise Exception("Chat not found")



async def is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False
    
async def is_valid_uz_phone(phone: str) -> bool:
    if not isinstance(phone, str):
        return False

    parts = phone.split(" ")

    # Format: +998 XX XXX XX XX → 6 ta qism bo‘lishi kerak
    if len(parts) != 6:
        return False

    country, operator, part1, part2, part3, part4 = parts

    # +998 tekshiruvi
    if country != "+998":
        return False

    # Operator kodi: 90–99
    if not operator.isdigit() or len(operator) != 2:
        return False
    if not (90 <= int(operator) <= 99):
        return False

    # Qolgan qismlar raqam va uzunliklari
    if not (part1.isdigit() and len(part1) == 3):
        return False
    if not (part2.isdigit() and len(part2) == 2):
        return False
    if not (part3.isdigit() and len(part3) == 2):
        return False
    if not (part4.isdigit() and len(part4) == 2):
        return False

    return True
