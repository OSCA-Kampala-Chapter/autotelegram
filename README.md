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
https://github.com/OSCA-Kampala-Chapter/autotelegram/archive/refs/tags/autotelegram-0.2.0-beta.zip
```

### Getting started
autotelegram cares about developer productivity, and that's why it tries to abstract away the tedious
and laborious complex code needed to develop telegram bots and provides you a nice and clean API to 
help you quickly spin-up a telegram bot in minutes. You wanna see how it works? let's get started
by building a simple echo bot.
With the previous API, we had to do a lot of manual work using the context API. If you still want to use
the context API, it's availabe for us. But the new API builds on top of the context API to give you a nice
interface to build a bot.

Before we can proceed building our bot, we need to create a bot in telegram and get our token.
To get one, we need to create a bot with telegram's bot father. You can get detailed instruction on how to
do that [here](https://core.telegram.org/bots/features#creating-a-new-bot)

Now that we have our token. Let me show you how easy it is to create a bot with autotelegram.
First, we need to import the `Context` and `PollingApp` classes and then write an async function we shall
pass to the `PollingApp` run method to process every incoming update. Here's how.
```python
from autotelegram.telegram.context import Context
from autotelegram.telegram.application import PollingApp

TOKEN = "token-for-the-bot"
ctx:Context = Context(TOKEN)
app = PollingApp(ctx)

async def echo (update,ctx):
    message = update.message
    text = message.text
    await message.respond_with_text(text)
    
if __name__ == "__main__":
    app.run(echo)
```
So basically here's a break down of this simple app.
we create an instance of the `Context` class, passing in the bot token.
We then create an instance of our `PollingApp` class and pass in the context instance.
Then we write our `echo` async function which shall respond back to every message with
the same text that was sent to it. 
We then call the run function of the app with the echo async function.
