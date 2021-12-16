from .models import (
    database, objects, TGUser, ReferralCabinet,
    Order, referral_cabinet_tgusers_through,
    ExchangeRate,
    migrate, migrator, DoesNotExist
)

def setup():
    TGUser.setup()
    ReferralCabinet.setup()
    Order.setup()
    ExchangeRate.setup()

    if not referral_cabinet_tgusers_through.table_exists():
        referral_cabinet_tgusers_through.create_table()
        
    
