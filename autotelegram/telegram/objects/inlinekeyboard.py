from autotelegram.telegram.objects.base import BaseObject
from autotelegram.telegram.objects.webapp import WebAppInfo
from autotelegram.telegram.objects.loginurl import LoginUrl
from typing import Optional,Literal

class CallbackGame(BaseObject):
    """
    A placeholder, currently holds no information. 
    Use BotFather to set up your game.
    """
    pass


class InlineKeyboardButton(BaseObject):

    """"
    
        This object represents one button of an inline keyboard. You must use exactly one of the optional fields.
        Args:
            text (str) : Label text on the button
            url	 (str) : Optional. HTTP or tg:// URL to be opened when the button is pressed. 
            Links tg://user?id=<user_id> can be used to mention a user by their ID without using a username, 
            if this is allowed by their privacy settings.
            callback_data (str) : Optional. Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes
            web_app (:obj:`WebAppInfo`) : Optional. Description of the Web App that will be launched when the user presses the button. 
            The Web App will be able to send an arbitrary message on behalf of the user using the method answerWebAppQuery. 
            Available only in private chats between a user and the bot.
            login_url (:obj:`LoginUrl`) : Optional. An HTTPS URL used to automatically authorize the user. 
            Can be used as a replacement for the Telegram Login Widget.
            switch_inline_query (str) : Optional. If set, pressing the button will prompt the user to select one of their chats, 
            open that chat and insert the bot's username and the specified inline query in the input field. May be empty, 
            in which case just the bot's username will be inserted.
                Note: This offers an easy way for users to start using your bot in inline mode when they are currently in a private chat with it. 
                Especially useful when combined with switch_pm… actions - in this case the user will be automatically returned to the chat they switched from, 
                skipping the chat selection screen.
            switch_inline_query_current_chat (str) : Optional. If set, pressing the button will insert the bot's username and the specified inline query 
            in the current chat's input field. May be empty, in which case only the bot's username will be inserted.
                This offers a quick way for the user to open your bot in inline mode in the same chat - good for selecting something from multiple options.
            callback_game (:obj:`CallbackGame`) : Optional. Description of the game that will be launched when the user presses the button.
                Note: This type of button must always be the first button in the first row.
            pay (bool) : Optional. Specify True, to send a Pay button.
                Note: This type of button must always be the first button in the first row and can only be used in invoice messages.
    """
    

    def __init__(self, text: str = None) -> None:
        self.text = text
        self.url: Optional[str] = None
        self.callback_data: Optional[str] = None
        self.web_app: Optional[WebAppInfo] = None
        self.login_url: Optional[LoginUrl] = None
        self.switch_inline_query: Optional[str] = None
        self.switch_inline_query_current_chat: Optional[str] = None
        self.callback_game: Optional[CallbackGame] = None
        self.pay: Optional[bool] = None
        

KeyboardType = Literal["stack","grid"]

class InlineKeyboardMarkup(BaseObject):


    """"
    
        This object represents an inline keyboard that appears right next to the message it belongs to.
        Args:
            keyboard_type (str): The type of keyboard to create. The value can either be "stack"
            which creates a stacked keyboard or "grid" which creates a grid keyboard

            cols (int): The number of columns to create if keyboard_type is "grid". Defaults to 2

            inline_keyboard (list[:obj:`InlineKeyboardButton`]) : Array of button rows, each represented by an Array of InlineKeyboardButton objects
        Examples:
            ```python
            from autotelegram.telegram.objects import InlineKeyboardMarkup
            
            keyboard = InlineKeyboardMarkup()
            keyboard.add_button("one",callback_data="1")
            keyboard.add_button("two",callback_data="2")
            keyboard.add_button("three",callback_data="3")
            board = keyboard.keyboard()
            ```    
    """
    

    def __init__(self, 
                 keyboard_type:Optional[KeyboardType] = "stack",
                 cols:int = 2,
                 inline_keyboard: list[InlineKeyboardButton] = None
                 ) -> None:
        
        self.keyboard_type = keyboard_type
        self.cols = cols
        self.inline_keyboard = inline_keyboard
        
        cols = self.cols if self.keyboard_type == "grid" else None
        self._keyboard = Keyboard(self.keyboard_type,cols)

    def add_button (self,text,**kwargs):
        """
        Add InlineKeyboardButton to the keyboard. The buttons will be arranged according to the 
        type of the keyboard set by keyboard_type option.
        Args:
            text: The text to place on the InlineKeyboardButton
            **kwargs: One of the options that are documented in InlineKeyboardButton class
        """
        kb_btn = InlineKeyboardButton(text)
        if kwargs:
            for k,v in kwargs.items():
                setattr(kb_btn,k,v)
        self._keyboard.add_button(kb_btn)

    def keyboard (self):
        """
        returns a rendered keyboard to be used in the `reply_markup` argument of message methods.
        """
        kb = {}
        kb["inline_keyboard"] = self._keyboard.keyboard()
        return kb
    



class Keyboard (list):

    class GridRow (list):
        """
        class representing a row in the InlineKeyboard
        """
        def __init__ (self,maxsize):
            self.maxsize = maxsize
            super(Keyboard.GridRow,self).__init__()

        def append (self,item):
            if len(self) < self.maxsize:
                super().append(item)
                return
            raise ValueError
        
    def __init__ (self,kb_type,cols = None):
        from autotelegram.telegram.parser import Composer

        self.kb_type = kb_type if kb_type in ["stack","grid"] else None
        self.cols = cols
        self.cur_row = None
        self._composer = Composer()
        super(Keyboard,self).__init__()

    def add_button (self,btn):
        kb_btn = self._composer.compose(btn)

        if self.kb_type == "stack":
            self.append([kb_btn])

        elif self.kb_type == "grid":
            if self.cur_row:
                try:
                    self.cur_row.append(kb_btn)
                except ValueError:
                    new_row = self.GridRow(self.cols)
                    new_row.append(kb_btn)
                    self.cur_row = new_row
                    self.append(self.cur_row)
            else:
                new_row = self.GridRow(self.cols)
                new_row.append(kb_btn)
                self.cur_row = new_row
                self.append(self.cur_row)

        else:
            raise ValueError("Invalid keyboard type")
        
    def keyboard (self):
        return self
