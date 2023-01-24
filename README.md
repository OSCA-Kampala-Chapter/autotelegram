# Autotelegram
![autotelegram](./docs/assets/autotelegram.png)

Autotelegram is a python library to help you build telegram bots fast and effeciently.
It is a spin-off of the autobot projects which focuses on helping you build telegram bots.
Autobot provides a pythonic wrapper around the telegram bot API to enable you make queries 
to you telegram bot directly from python code

### Installation
Installing autotelegram on your system is a s easy as pip installing it. Just copy and paste
the snippet below in your command line

```
pip install https://github.com/OSCA-Kampala-Chapter/autotelegram/archive/refs/tags/autotelegram-0.0.1b2.zip
```

### Tutorial
To understand how autotelegram works, let us build a simple echo bot that echos back what the user
sends to it.
Before we go any further, we need to create a telegram bot and get its API key. To create a telegram bot,
you need to talk to the botfather. You can follow detailed instructions on hoe to create a telegram bot 
[here](https://core.telegram.org/bots#how-do-i-create-a-bot)

Alright, now that we have a token, we shall start off building our bot. Autotelegram wraps the entire interface
to your bot in a bot context class. This means that you only need to call methods on this bot context to interact
with your bot. we start by importing context from `autotelegram.telegram.context`
```python
from autotelegram.telegram.context import Context
```
autotelegram is built on top os asyncio, so that means we'll need to import it as well in order to call some methods
on the bot context.
```python
from autotelegram.telegram.context import Context
import asyncio
```
Now that we have context and asyncio imported, time to start building our bot.
Basically this is what our bot is going to be doing. It will get updates from telegram about anyone that interacted 
with our bot and the work on those updates. Telegram provides two methods to receive updates from the bot. We can either 
use `getUpdates` method or set a webhook so that telegram notifies us of any activity on the bot. For now, we shall focus 
on the `getUpdates` method as we don't have a dedicated server to set webhooks. Not that we shall bot use `getUpdates`
but rather `get_updates`, autotelegram provides the same methods as those of telegram but witha more pythonic look, which 
is the snake-case as it's formally known.

Telegram also provides us a url to our bot so that we can receive and send updates to it. The url is in the form of
`https://api.telegram.org/bot<TOKEN>/`.
TOKEN is the token string we've received from BotFather about the address of our bot. 
There is not space between bot and the Token. You don't have to worry about this as autotelegram manages the
URL for you. All you need to do is provide the token to the context

Alright, now that we've gotten the basics out of the way, let's code up a functional bot with autotelegram.
The program will be making requests to the bot API, processing the results and sending back results to the bot.
To reduce the frequency at which requests are made, we'll tell the program to sleep for 10 seconds before
making requests to the bot again. We now also store a token in the TOKEN variable as a string
```python
from autotelegram.telegram.context import Context
import asyncio
import time

TOKEN = "your bot token"

async def main ():
    bot = Context(TOKEN)
    while True:
        updates = await bot.get_updates()
        for update in updates:
            if (msg := update.message):
                cid = msg.chat.id            # the ID of the chat that sent the message
                txt = msg.text               # the message which was sent
                await bot.send_message(chat_id = cid, text = txt)     # send the message back to the sender
                
        time.sleep(10)
        
if __name__ == "__main__":
    asyncio.run(main())
```
The main function contains all the logic of our bot. Let's go through it to understand how it works.
First we created out bot context with the TOKEN. This is our interface for interacting with the telegram bot.
we immediately start an infinte loop to run our program recuringly. 
We await on the async `get_updates`method of the bot context to receive updates.
Telegram provides us updates inform of a JSON Object. To make the response easier to interact with,
we parse the JSON into a tree of objects representing the different telegram objects. Telegram represents
every element of the application such as message, sticker, voicenote, document, picture, url link and so 
many other elements as Telegram objects. In our program, we're accessing the message object and reading its
chat and text values. The Chat object represents the chat from which the message came from, and it had an `id`
parameter which uniquely identifies this chat. The chat could be another user or group or channel.

After getting the text and id of the chat we got the message from, we use the `send_message` method on
the bot to send back a message to chat. we specify the `chat_id` to send the text to and `'text` to send.
There are other optional parameters we can pass to `send_message` as documented in the telegram bot API docs.
The program will sleep for 10 seconds and the resume. To close the program, press CTRL-Z.

*Note: On windows, a RuntimeError is raised when the program is closing. This is an internal issue with the
default proactor event loop and can safely be ignored as of now.*

We have successfully built our first telegram bot. And boy was that easy to do. Remember, autotelegram
provides a pythonic wrapper around the telegram bot API. This means that to understand autotelegram,
you have to go through the telegram bot api documentation as well. You can find the documentation [here](https://core.telegram.org/bots/api)
It will also be useful for you to read an introduction to telegram bots and what they can do [here](https://core.telegram.org/bots)

For any questions, please use our discussions and we'll be able to help you out.
