from asyncio import run, gather

import handlers, utils
from data.loader import dp, bot
from utils.misc.helpers import start_bot
from utils.misc.db import create_pool, create_tables_if_not_exist


async def main() -> None:

    await create_pool()
    await create_tables_if_not_exist()

    dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)

    gather(await dp.start_polling(bot))


if __name__ == "__main__":
    # basicConfig(level=INFO, stream=stdout)
    run(main())

