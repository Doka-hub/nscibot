from pathlib import Path

from decouple import config


# PATH settings
BASE_DIR = Path(__file__).parent.parent
LOGS_BASE_PATH = str(BASE_DIR / 'logs')


# BOT settings
BOT_PLACE = config('BOT_PLACE', 'locale')

BOT_TOKEN = config('BOT_TOKEN')

BASE_URL = config('BASE_URL')  # webhook domain
ADMINS = [
    539655707,  # Дока
    287478166,
    1590525561,
#    863053395,
    300061390
]
MODERATOR_USERNAME = 'NSCI_support'
HELPER_USERNAME = 'NSCI_support'

# WEBHOOK settings
WEBHOOK_PATH = f'/tg/webhooks/bot/'
WEBHOOK_URL = f'{BASE_URL}{WEBHOOK_PATH}{BOT_TOKEN}'

# I18N settings
I18N_DOMAIN = 'bot'
LOCALES_DIR = BASE_DIR / 'locales'

# TIMEZONE
TIMEZONE = config('TIMEZONE')

# DATABASE
DATABASE = config('DATABASE')

POSTGRESQL = {
    'bot': {
        'host': config('POSTGRESQL_HOST', 'localhost'),
        'user': config('POSTGRESQL_USER', 'postgres'),
        'db': config('BOT_DATABASE_NAME', 'nscibot')
    }
}

MYSQL = {
    'bot': {
        'host':     config('MYSQL_HOST', 'localhost'),
        'user':     config('MYSQL_USER', 'root'),
        'password': config('MYSQL_PASSWORD', None),
        'db':       config('BOT_DATABASE_NAME', None),
        'maxsize':  5,
        'port':     3306
    }
}

REDIS = {
    'ip':     config('REDIS_URL', 'redis://127.0.0.1'),
    'port': config('REDIS_PORT', 6379)
}
