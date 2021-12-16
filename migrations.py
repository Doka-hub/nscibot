from playhouse.migrate import CharField, DecimalField, BooleanField, IntegerField, ForeignKeyField

# local imports
from models import bot

'''Здесь прописывать миграции'''
if __name__ == '__main__':
    bot.migrate(
        # bot.migrator.add_column('tguser', 'referrer_user_id', 
        #     IntegerField(null=True, verbose_name='ID пригласителя в БД')
        # ),
        # bot.migrator.drop_column('tguser', 'referral_user_id')
        bot.migrator.alter_add_column(
            'referralcabinet', 'tguser',
            ForeignKeyField(bot.TGUser, on_delete='CASCADE', unique=True, backref='referral_cabinet', verbose_name='Реферальный кабинет')
        )
    )
    # referral_user_id = IntegerField(null=True, verbose_name='ID пригласителя в БД')
    pass
