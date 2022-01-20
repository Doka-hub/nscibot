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
            'tguser', 'user_id',
            CharField(max_length=255, verbose_name='ID')
        )
    )
    # referral_user_id = IntegerField(null=True, verbose_name='ID пригласителя в БД')
    pass
