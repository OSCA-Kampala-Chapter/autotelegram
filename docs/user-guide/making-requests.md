### Overview
Telegram provides an HTTP based API to interact with the bot. You can send `GET` or `POST` requests to the API to pass instructions to the bot and receive back success data if the request was successful or JSON error data if the request was not successful.

#### Getting token
Telegram provides a url of the form `https://api.telegram.org/bot<TOKEN>/` to interact with your bot.
`<TOKEN>` is your unique token identifying your bot. You can get this token from the botfather telegram bot which is used to create telegram bots. You can follow instruction [here](https://core.telegram.org/bots/features#creating-a-new-bot) to create your bot and get a token.

### Making requests
With a token, we can now manually interact with our bot. Let us test and see.
```python
>>> from urllib.request import urlopen
>>> from pprint import PrettyPrinter
>>> import json

>>> token = "your-telegram-token"
>>> api_url = "https://api.telegram.org/bot"
>>> bot_api_url = api_url + token
>>> 
>>> pp = PrettyPrinter()
>>> with urlopen(bot_api_url + "/getMe") as f:
...     pp.pprint(json.loads(f.read().decode()))
...

```
The `getMe` method returns a `User` object describing the bot.
you'll see a pretty printed result of the request which describes your bot. It will look something like
```JSON
{"ok":true,
"result":{
    "id":5083423735,
    "is_bot":true,
    "first_name":"Sanyu",
    "username":"OscaKampBot",
    "can_join_groups":true,
    "can_read_all_group_messages":false,
    "supports_inline_queries":false}}
```

### The context api
However, working with a telegram bot this way can be very tedious and time consuming. You'll have to account for network failures, parsing different kinds of results, handling request data such forms and multimedia and so many other things you'll have to build from scratch to have a decently functioning bot.

Autotelegram builds a nice async wrapper over the bot api and encapsulates all the telegram methods in  a `Context` object.
The `Context` object now becomes the representation of our telegram bot to us. We can interact with the bot via calling methods on the `Context` api which will make reliable requests for us under the hood and also manage the network connection, parsing of various data and so on. Here's how we would rewrite the above example with the `Context` object from autotelegram.
```python
>>> import asyncio
>>> from pprint import PrettyPrinter
>>> from autotelegram.telegram.context import Context
>>>
>>> token = "your-telegram-token"
>>> bot = Context(token)
>>> pp = PrettyPrinter()
>>> 
>>> async def main ():
...     me = await bot.get_me()
...     pp.pprint(vars(me))
...
>>>
>>> asyncio.run(main())
```
you will get a print-out similar to the one in the first manual request. Though this time round, you'll only get a print-out of the actual user object JSON returned, without the `ok` element.
The `Context` api supports all methods from telegram. The only difference is that they are formatted into **snake case** instead of the **camel case** from the actual telegram api.
So that means `getMe` on the telegram bot api will be called as `get_me` on the context api. And `sendMessage` on the telegram bot api will be called as `send_message` on the context api.
The context api interally parses the JSON result and returns a nice telegram object tree to easily interact with like we elaborated in the previous page.

### The application
Whereas the context API provides a nice wrapper around the telegram bot API. It's also quite as low level as making requests manually. Indeed perhaps we will have to implement a loop which periodically makes request and handles the updates.

Instead of doing that, autotelegram comes with an application class that implements the `PollingApp`.
The PollingApp is responsible for making periodic requests to the bot api and calling a handler async function with each update that it receives. This greatly simplifies the development process, all you have to write is an async function callback to be called on each update. The application class manages the context API for us, so we still have to pass the `Context` to the application class. Here's how
```python
>>> from autotelegram.telegram.context import Context
>>> from autotelegram.telegram.application import PollingApp
>>> 
>>> token = "your-telegram-token"
>>> context = Context(token)
>>> bot = PollingApp(context)
>>> 
>>> async def main (update,context):
...     print("received update: ",update.update_id)
...
>>> bot.run(main)
```
The application will start a loop calling `main` on every update it gets. the callback fuction to pass to the run method should be an async function with a signature of </br>
`async callback (update,context):`
The `update` is the update object received and the `context` is the encapsulation of the bot and the context API.
The application class provides us a way of easily customizing responses to certain requests, error handling and so much much more that we shall explore later in the documentation.
