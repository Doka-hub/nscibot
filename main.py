from typing import List

from asyncio import sleep

from aiohttp import web

import aiojobs as aiojobs

from aiogram import Bot, bot

from loguru import logger

# local imports
from data import config

from loader import bot_dp


async def on_startup(app: web.Application):
    import models
    import middlewares
    import filters
    import handlers

    models.setup()
    middlewares.setup(bot_dp)
    filters.setup(bot_dp)
    handlers.setup(bot_dp)

    logger.info('Configure BOT Webhook URL to: {url}', url=config.WEBHOOK_URL)
    
<<<<<<< HEAD
#    await bot_dp.start_polling()
    await bot_dp.bot.set_webhook(config.WEBHOOK_URL)
=======
    # await bot_dp.start_polling()
    # await bot_dp.bot.set_webhook(config.WEBHOOK_URL)
>>>>>>> de7224ce563fb2003c851b765acfc93b4961e99c
    # await sleep(2)


async def on_shutdown(app: web.Application):
    await bot_dp.bot.close()
    return
    # await subscriber_dp.bot.delete_webhook()
    # await subscriber_dp.bot.close()


async def init() -> web.Application:
    from utils.misc import logging
    import web_handlers
    logging.setup()
    scheduler = await aiojobs.create_scheduler()
    app = web.Application()
    subapps: List[str, web.Application] = [
        ('/tg/webhooks/', web_handlers.tg_updates_app),
        ('/static/', web_handlers.static_app),
        ('/admin/', web_handlers.admin_app),
    ]
    for prefix, subapp in subapps:
        subapp['bot'] = bot_dp.bot
        subapp['dp'] = bot_dp

        subapp['scheduler'] = scheduler
        app.add_subapp(prefix, subapp)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


if __name__ == '__main__':
    web.run_app(init(), host=['0.0.0.0'], port='8000')
