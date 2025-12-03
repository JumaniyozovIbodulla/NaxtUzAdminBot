from asyncio import run, gather

import handlers, utils
from data.loader import dp, bot
from utils.misc.helpers import start_bot



async def main() -> None:

    dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)

    gather(await dp.start_polling(bot))


if __name__ == "__main__":
    # basicConfig(level=INFO, stream=stdout)
    run(main())

