# # from peewee_async import Manager, MySQLDatabase
# #
# # database = MySQLDatabase(
# #     database='opt_www',
# #     user='admin',
# #     password='VCbH#dh_Sc9c+3_A',
# #     host='176.107.186.4'
# # )
# # objects = Manager(database)
# #
# #
# # products = database.execute_sql(
# #     'SELECT * FROM modx_ms2_products WHERE article="DR_203932";')
# #
# #
# # vendor_id = products.fetchone()[7]
# # print(vendor_id)
# #
# # vendor = database.execute_sql(
# #     f'SELECT * FROM modx_ms2_vendors WHERE id={vendor_id};')
# # print(vendor.fetchone())
# # import asyncio

# from models import bot
# from models.bot.models import TGUser
# # bot.database.drop_tables(
# #     [
# #         bot.ReferralCabinet, bot.referral_cabinet_tgusers_through,
# #         bot.TGUser, bot.Order
# #     ]
# # )
# user = TGUser.select().where(TGUser.username == 'Hogwartsexpressus').get()
# print(user.get_active_referrals_count())

# # user = TGUser.select().execute()[0]


# # print([i for i in user.orders])
# # for i in users:
# #     for referral in i.referral_cabinet.get().referrals.execute():
# #         # print(referral.username)
# #         referral.referrer_user_id = 1
# #         referral.is_referral = True
# #         referral.save()

# # print(
# #     [[x for x in i.referral_cabinet.get().referrals.select()] for i in TGUser.select()]
# # )

# # from utils.bot.db_api.order.order import get_user_list_to_send_orders
# # from tasks.bot.mail import orders_send

# # #
# # #
# # loop = asyncio.get_event_loop()
# # loop.run_until_complete(
# #     orders_send()

# # )
# #
# # user_list = loop.run_until_complete(get_user_list_to_send_orders())
# #
# #
# # async def ex():
# #     return await objects.execute(user.orders)
# #
# #
# # for user in user_list:
# #     print(user)
# #     # print(
# #     #     *loop.run_until_complete(ex())
# #     # )
# #
# #
# import time
# import requests as r
# from threading import Thread
#
# from time import sleep
#
#
# def req():
#     resp = r.get('https://instastar.link/api/sub.php?username=lal123123123123&uuid=e71bd3bf-db49-425c-9486-aeca6e1bc96a&h=cf793f2f8514f88ff49bad48772ce0b3')
#     print(resp)
#
#
# threads = []
#
#
# for i in range(100):
#     thread = Thread(target=req)
#     threads.append(thread)
#
#
# for thread in threads:
#     thread.start()
#     thread.join()
import asyncio

from loader import bot_dp


async def main():
    print(await bot_dp.bot.set_webhook('https://bot.optovi4ok.top/tg/webhooks/bot/1686187148:AAGZx5EwhDUtOaCwgAcv4uicXbknZxiTmoM'))


asyncio.run(main())