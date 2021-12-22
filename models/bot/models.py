from typing import List

import peewee
from peewee import DoesNotExist
from peewee_async import Manager, PostgresqlDatabase, MySQLDatabase

from playhouse.migrate import MySQLMigrator, PostgresqlMigrator, migrate

# local imports
from data import config

from .fields import JSONField


if config.DATABASE == 'mysql':
    database = MySQLDatabase(
        host='sql4.freesqldatabase.com',
        database='sql4459166',
        user='sql4459166',
        password='nKMh9Em8Ql'
    )
    migrator = MySQLMigrator(database)
elif config.DATABASE == 'postgresql':
    database = PostgresqlDatabase(database=config.POSTGRESQL['bot']['db'],
                                  user=config.POSTGRESQL['bot']['user'])
    migrator = PostgresqlMigrator(database)
objects = Manager(database)


class BaseModel(peewee.Model):
    class Meta:
        database = database

    @classmethod
    def setup(cls):
        if not cls.table_exists():
            cls.create_table()


class TGUser(BaseModel):
    LANGUAGE_CHOICES = (
        ('ru', 'ru'),
        ('en', 'en'),
    )

    user_id = peewee.IntegerField(verbose_name='ID')
    username = peewee.CharField(max_length=255, null=True, verbose_name='Логин')
    full_name = peewee.CharField(max_length=255, null=True, verbose_name='Имя')
    phone_number = peewee.CharField(max_length=255, null=True, verbose_name='Номер телефона')

    language = peewee.CharField(max_length=3, null=True, choices=LANGUAGE_CHOICES, verbose_name='Язык')

    balance = peewee.DecimalField(default=0, verbose_name='Баланс')
    earned = peewee.DecimalField(default=0, verbose_name='Заработано')
    
    notifications_subscribed = peewee.BooleanField(default=False, verbose_name='Подписан на уведомления')

    is_referral = peewee.BooleanField(default=False, verbose_name='Реферал')
    referrer_user_id = peewee.IntegerField(null=True, verbose_name='ID пригласителя в БД')

    bot_blocked_by_user = peewee.BooleanField(default=False, verbose_name='Бот заблокирован пользователем')
    is_active = peewee.BooleanField(default=True, verbose_name='Активный')

    def get_active_referrals_count(self):
        active_referrals = 0
        for referral in self.referral_cabinet.get().referrals:
            print(referral)
            if referral.orders.filter(Order.paid == True):
                active_referrals += 1
        return active_referrals

    def get_referrals_count(self):
        return self.referral_cabinet.get().referrals.count()
    
    async def get_bought_amount(self):
        amount = 0
        orders: List[Order] = await objects.execute(self.orders.filter(Order.paid == True))
        for order in orders:
            amount += order.amount
        return amount
    
    def __str__(self):
        return self.username or str(self.id)
    

class ReferralCabinet(BaseModel):
    tguser = peewee.ForeignKeyField(TGUser, on_delete='CASCADE', unique=True, backref='referral_cabinet', verbose_name='Реферальный кабинет')
    
    referral_link = peewee.CharField(verbose_name='Реферальная сссылка')
    referrals = peewee.ManyToManyField(TGUser, backref='referrals')


referral_cabinet_tgusers_through = TGUser.referrals.get_through_model()


class Order(BaseModel):
    tguser = peewee.ForeignKeyField(TGUser, on_delete='CASCADE',  backref='orders', verbose_name='Заказы')

    amount = peewee.DecimalField(verbose_name='Сумма')
    paid = peewee.BooleanField(default=False, verbose_name='Оплачено')

    created = peewee.DateTimeField(verbose_name='Создано')

    def __str__(self):
        return self.tguser.username or self.tguser.id


class ExchangeRate(BaseModel):
    cost = peewee.DecimalField(verbose_name='Цена')

    @classmethod
    def setup(cls):
        if not cls.table_exists():
            cls.create_table()
            cls.create(cost=100)


class MessageTemplate(BaseModel):
    user = peewee.ForeignKeyField(TGUser, on_delete='CASCADE',
                                  related_name='message_templates')

    name = peewee.CharField(max_length=255, unique=True)
    data = JSONField()

