from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from redis.asyncio import Redis
from aiogram.client.default import DefaultBotProperties
from data import config
from aiogram.enums import ParseMode

router = Router(name=__name__)
# Create bot
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# Create storage
redis = Redis.from_url(
    config.REDIS_URL,
    decode_responses=True,
    max_connections=20
)
storage = RedisStorage(redis, DefaultKeyBuilder(with_destiny=True), state_ttl=60*60*20, data_ttl=60*60*24) # 1 kun saqlanadi sessionlar

# Create dispatcher with storage
dp = Dispatcher(storage=storage)

dp.include_router(router)

