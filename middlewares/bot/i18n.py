from typing import Tuple, Any, Optional

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

# local imports
from utils.bot.db_api.user.language import get_language

from data.config import I18N_DOMAIN, LOCALES_DIR


class LanguageMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        chat = types.Chat.get_current()
        if chat.type != 'channel':
            user = types.User.get_current()
            lang = await get_language(user_id=user.id) or user.locale
            return lang

    def gettext(self, singular, plural=None, n=1, locale=None):
        if locale is None:
            locale = self.ctx_locale.get()

        if locale not in self.locales:
            if n == 1:
                return singular
            return plural

        translator = self.locales[locale]
        if plural is None:
            text = translator.gettext(singular)
        else:
            text = translator.ngettext(singular, plural, n)
        print('text: ', text)
        return text


i18n = LanguageMiddleware(I18N_DOMAIN, LOCALES_DIR)
