"""
This module contains the context of the telegram bot
"""

from autotelegram.telegram.api import BotAPI
from autotelegram.telegram.games.api import GamesAPI
from autotelegram.telegram.inline.api import InlineAPI
from autotelegram.telegram.passport.api import PassportAPI
from autotelegram.telegram.payments.api import PaymentsAPI
from autotelegram.telegram.stickers.api import StickerAPI
from autotelegram.network.connection import HTTPConnection
from autotelegram.network.urlmanager import UrlManager
from autotelegram.telegram.parser import Parser,Composer
import json

class TelegramResultError(Exception):
    """
    raised when telegram returns "ok" as false
    """


class Context(
    BotAPI,
    GamesAPI,
    InlineAPI,
    PassportAPI,
    PaymentsAPI,
    StickerAPI
):
    parser = Parser()

    composer = Composer()

    def __init__ (self,
        token,*,
        connection = None,
        offset_autoincrement = True
    ):
        """
        Context acts as the representation of the telegram bot
        """
        self.offset_autoincrement = offset_autoincrement
        self._latest_update = 0
        self.url = UrlManager(token)
        self.connection = connection if connection else HTTPConnection()
        self._set_current_context()

    async def _get (self,*,url = None,headers = None):
        """
        The _get method adds error handling on top of the abstract get method provided by
        the get method from the HTTPConnection object. If the return value is a success, that is
        it has "ok" as True, then it returns the json string. If "ok" is False, it extracts the 
        description of the failure and raises an error with the description
        """
        res = await self.connection.get(url,headers)
        return self._error_handler(res)

    async def _post (self,*,url = None,headers = None,body = None):
        """
        The _post method adds error handling on top of the abstract get method provided by
        the get method from the HTTPConnection object. If the return value is a success, that is
        it has "ok" as True, then it returns the json string. If "ok" is False, it extracts the 
        description of the failure and raises an error with the description
        """
        res = await self.connection.post(url,headers,body)
        return self._error_handler(res)

    def _error_handler(self,res):
        """
        This function does the actual error handling used in _get and _post
        """
        res = json.loads(res)
        if res["ok"]:
            return res["result"]
        error_code,desc = res["error_code"],res["description"]
        raise TelegramResultError(f"Error Code <{error_code}>:: {desc}")
    
    def _set_current_context (self):
        """
        This method sets the _current_context variable to self
        """
        global _current_context
        _current_context = self

    async def get_updates (self,**kwargs):
        """
        get updates from telegram. Automatically increases offset on next request
        """
        if self.offset_autoincrement:
            if "offset" in kwargs:
                kwargs.pop("offset")
            if self._latest_update:
                updates = await super().get_updates(offset = str(self._latest_update + 1),**kwargs)
                for update in updates:
                    if ((uid := update.update_id) > self._latest_update):
                        self._latest_update = uid
                return updates
            else:
                updates = await super().get_updates(**kwargs)
                return updates
        else:
            updates = await super().get_updates(**kwargs)
            return updates


"""
_current_context is an internal variable holding the reference to the current bot context.
It is set during the instantiation of the bot context and it's used by telegram objects
to offer extra functionality over the object.
"""
_current_context:Context = None

def get_current_context ():
    """
    this function returns  _current_context.
    """

    return _current_context

class MessageBox:
    """
    MessageBox is an object intended to be used for sending messages between
    telegram actors. The Messagebox contains The telegram object being transfered
    and the context object
    """

    def __init__ (self,telegram_object,context):
        
        self.telegram_object = telegram_object
        self.context = context