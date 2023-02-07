
from autotelegram.telegram.context import Context
import asyncio

__all__ = ("BaseApp","PollingApp")

class BaseApp (object):
    """
    The Telegram application 
    """
    def __init__ (self,context:Context) -> None:
        self._context = context
        self._commandhandlers = {}

    def add_commandhandler (self,command:str):
        """
        Registers a coroutine function to be called whenever the bot receives a command instruction
        from the user. The callback should accept one argument which is the bot context instance.
        Args:
            command: a string representing a command to add a handler to. The command should start with a forward slash '/'
        """

        def handler_func (callback):
            self._commandhandlers[command] = callback

        return handler_func
    
    def remove_commandhandler (self,command):
        """
        Remove command and respective callback from the register.
        Raises ValueError in case the command was not registered before.
        """

        try:
            self._commandhandlers.pop(command)
        except KeyError:
            raise ValueError(f"command {command} was not registered.")
        
    async def _runner (self,callback,wait_for):

        while True:
            updates = await self._context.get_updates()

            for update in updates:
                try:
                    msg = update.message.text
                    if msg.startswith("/"):
                        try:
                            cmd_handler = self._commandhandlers[msg]
                            await cmd_handler(update,self._context)
                        except KeyError:
                            await callback(update,self._context)
                    else:
                        await callback(update,self._context)
                except AttributeError:
                    """
                    message is None, so we assume there are other attributes such as
                    callback query or poll so we call the callback to process the update
                    """
                    await callback(update,self._context)

            await asyncio.sleep(wait_for)
            continue
        

class PollingApp(BaseApp):

    def run (self,callback,wait_for = 0):
        """
        Runs the bot application.
        Args:
            callback: coroutine function to be called for every update object received. This function should
            accept two arguments which are the update object and the bot context

            wait_for: integer representing the time in seconds to wait before requesting for updates

        """
        print("running now...") #add logging here
        

        asyncio.run(self._runner(callback,wait_for))