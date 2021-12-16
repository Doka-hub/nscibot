from aiohttp import web

import aiohttp_jinja2
import jinja2

from datetime import datetime

from decimal import Decimal

# local imports
from models.bot import objects, TGUser, Order, ExchangeRate


admin_app = web.Application()
aiohttp_jinja2.setup(admin_app, loader=jinja2.FileSystemLoader('templates'))


@aiohttp_jinja2.template('admin/admin.html')
async def admin(request: web.Request) -> dict:
    response = {}
    return response


# users
@aiohttp_jinja2.template('admin/users-list.html')
async def users(request: web.Request) -> dict:
    response = {}

    tguser_list = await objects.execute(TGUser.select())
    
    response['tguser_list'] = tguser_list
    return response


@aiohttp_jinja2.template('admin/users-detail.html')
async def users_detail(request: web.Request) -> dict:
    response = {}

    user_id = request.match_info['user_id']
    try:
        user = await objects.get(TGUser, id=user_id)
    except TGUser.DoesNotExist:
        user = None

    response['tguser'] = user
    response['referrals'] = user.referral_cabinet.get().referrals.execute()
    return response


@aiohttp_jinja2.template('admin/users-detail-referrals.html')
async def users_detail_referarls(request: web.Request) -> dict:
    response = {}

    user_id = request.match_info['user_id']
    try:
        user = await objects.get(TGUser, id=user_id)
    except TGUser.DoesNotExist:
        user = None

    response['tguser'] = user
    response['referrals'] = user.referral_cabinet.get().referrals.execute()
    return response

    
@aiohttp_jinja2.template('admin/users-list.html')
async def users_delete(request: web.Request) -> dict:
    user_id = request.match_info['user_id']
    try:
        user = await objects.get(TGUser, id=user_id)
    except TGUser.DoesNotExist:
        user = None

    if user:
        text = f'Пользователь {user} удален'
        await objects.delete(user)
    else:
        text = 'Пользователя не найден'
    return web.HTTPPermanentRedirect('/admin/users/list/', text=text)


# orders
@aiohttp_jinja2.template('admin/orders-list.html')
async def orders_list(request: web.Request) -> dict:
    response = {}
    
    order_list = await objects.execute(Order.select())

    response['order_list'] = order_list
    return response
    

@aiohttp_jinja2.template('admin/orders-detail.html')
async def orders_detail(request: web.Request) -> dict:
    response = {}

    order_id = request.match_info['order_id']
    try:
        order = await objects.get(Order, id=order_id)
    except Order.DoesNotExist:
        order = None

    response['order'] = order
    return response


@aiohttp_jinja2.template('admin/orders-create.html')
async def orders_create(request: web.Request) -> dict:
    response = {'errors': {}, 'values': {}}
    return response


@aiohttp_jinja2.template('admin/exchange-rate.html')
async def exchange_rate_detail(request: web.Request) -> dict:
    response = {'errors': {}, 'values': {}}

    exchange_rate = (await objects.execute(ExchangeRate.select()))[0]

    response['exchange_rate'] = exchange_rate
    return response


@aiohttp_jinja2.template('admin/exchange-rate.html')
async def exchange_rate_edit(request: web.Request) -> dict:
    response = {'errors': {}, 'values': {}}

    exchange_rate_data = await request.post()
    amount = exchange_rate_data.get('cost')

    exchange_rate = (await objects.execute(ExchangeRate.select()))[0]

    exchange_rate.cost = amount
    await objects.update(exchange_rate, ['cost'])

    response['exchange_rate'] = exchange_rate
    return response


@aiohttp_jinja2.template('admin/orders-create.html')
async def post_orders_create(request: web.Request) -> dict:
    response = {'errors': {}, 'values': {}}
    tguser = None

    order_data = await request.post()
    user_id = order_data.get('user_id')
    amount = order_data.get('amount')
    paid = order_data.get('paid')

    response['values'].update(
        {
            'user_id': user_id,
            'amount': amount,
            'paid': paid
        }
    )

    if user_id:
        try:
            tguser = await objects.get(TGUser, user_id=int(user_id))
        except TGUser.DoesNotExist:
            response['errors'].update({'user_id': 'Аккаунт не найден'})

        if tguser:
            order = await objects.create(Order, **{
                'tguser': tguser,
                'amount': int(amount),
                'paid': True if paid == '' else False,  # если пришло в пост дате, то paid отмечен в форме
                'created': datetime.now()
            })

            tguser.balance += order.amount
            await objects.update(tguser, ['balance'])
            
            if tguser.is_referral:
                print(tguser.referrer_user_id, type(tguser.referrer_user_id))
                try:
                    referrer = await objects.get(TGUser, id=int(tguser.referrer_user_id))
                    bonus = 0.02
                    if referrer.get_active_referrals_count() >= 10:
                        bonus = 0.08
                    amount = Decimal(order.amount * bonus)
                    referrer.balance += amount
                    referrer.earned += amount
                    await objects.update(referrer, ['balance', 'earned'])
                except TGUser.DoesNotExist:
                    pass
        response['values'] = {}
    return response


admin_app.add_routes(
    [
        web.get('/', admin),

        # users
        web.get('/users/list/', users),
        web.get('/users/detail/{user_id}/', users_detail),
        web.get('/users/detail/{user_id}/referrals/', users_detail_referarls),
        web.get('/users/detail/{user_id}/delete/', users_delete),

        # orders
        web.get('/orders/list/', orders_list),

        web.get('/orders/create/', orders_create),
        web.post('/orders/create/', post_orders_create),

        web.get('/orders/detail/{order_id}/', orders_detail),

        # exchange rate
        web.get('/exchange-rate/', exchange_rate_detail),
        web.post('/exchange-rate/', exchange_rate_edit),
    ]
)
