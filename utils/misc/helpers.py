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
    
