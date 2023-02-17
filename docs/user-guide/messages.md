
Messages are one of the central concepts in telegram. since telegram is a messaging application, a lot of updates passed to telegram bots come as message objects.
Message objects represent any text, video, image, voice-note, document or any other form of data being exchanged on telegram. However, telegram adds other features for bots to make messages more expressive on the telegram client.

### Attributes
The `Message` object has the most attributes of any telegram object, it contains a `message_id` to uniquely identify that message in a given chat, has `message_thread_id` to show the exact forum topic the message was sent to (that is if the group has forum topics set), has `text` attribute which contains the text that we have received from the user via the bot interaction and so many other attributes we can query to determine the origin and state of the message.
```python
>>> message = update.message
>>> message.message_id
749248928
>>> message.text
"/start"
```
You can view a complete list of the message attributes over at the reference pages [here](../reference/objects/gen/message.md).

### Methods
#### respond
Other than just querying message objects for their state and data, we can also manipulate messages to offer responses or replies.
Using the `respond_with_text` method, we can respond to any message with a text message. All methods that require sending and receiving data to and from telegram are **async** and require to be **awaited** on.
```python
from autotelegram.telegram.context import Context
from autotelegram.telegram.application import PollingApp

TOKEN = "token-for-the-bot"

ctx = Context(TOKEN)
app = PollingApp(ctx)

async def main (update,ctx):
    message = update.message
    text = "Thanks for contacting health-line, how can we help?"
    await message.respond_with_text(text)
    
if __name__ == "__main__":
    app.run(main)
```
#### reply
We can also reply to messages directly in the chat using the `reply_with_text` method.
```python
async def main (update,ctx):
    message = update.message
    text = "Thanks for contacting health-line, how can we help?"
    await message.reply_with_text(text)
    
if __name__ == "__main__":
    app.run(main)
```
#### replace
We can also replace a sent message with a new message. This is very useful in cases where you wouldn't want to constantly send messages to the user. You can just replace an already sent message with a new one. For example, a user viewing a menu by a certain restaurant doesn't need to be sent messages for every item on the menu, the message containing the menu list can constantly be updated as the client browses through the options. This creates an illusion of swiping in some case.
To replace a message, you can use `replace_with_text` method.
```python
async def main (update,ctx):
    message = update.message
    text = "Thanks for contacting health-line, how can we help?"
    await message.respond_with_text(text)
    await asyncio.sleep(2)
    await message.replace_with_text("original text has been replaced.")
    
if __name__ == "__main__":
    app.run(main)
```
#### delete
You can also entirely delete messages from telegram. To do this, use the `delete_message` method
```python
async def main (update,ctx):
    message = update.message
    text = "Thanks for contacting health-line, how can we help?"
    await message.respond_with_text(text)
    await asyncio.sleep(2)
    await message.delete_message()
    
if __name__ == "__main__":
    app.run(main)
```
### sending keyboards
Telegram has a concept of "keyboards", these are custom input interfaces that telegram clients create on the bot's behalf to replace direct text input with predefined options sent by the bot.
You can read more about keyboards [here](https://core.telegram.org/bots/features#keyboards). Autotelegram helps you easily create and send keyboards along with your messages. There are 2 kinds of keyboards, The Inline Keyboard and Reply Keyboard. Let's check the Inline Keyboard first.

#### Inline Keyboards
Telegram has a feature called Inline Keyboard. These are a set of options sent along with a telegram message to a user or client. To create an Inline Keyboard, we import the `InlineKeyboardMarkup` class.
```python
from autotelegram.telegram.objects import InlineKeyboardMarkup as keyboard
```
We can then create an instance of the keyboard. `InlineKeyboardMarkup` supports creation of **"stack"** or **"grid"** shaped keybaords depending on the first argument you pass the constructor during instantiation. By default, it will create a stack keyboard.
```python
kb = keyboard("stack")
```
We can now add buttons to the keyboard which will be arranged in a stack.
```python
kb.add_button("minor",callback_data = "min")
kb.add_button("moderate",callback_data = "mod")
kb.add_button("major",callback_data = "maj")
kb.add_button("severe",callback_data = "sev")
```
We have now added 4 buttons to our keyboard. The buttons are represented by `InlineKeyboardButton` and they take in a couple of optional parameters. One of the parameters is `callback_data`. This is data that shall be sent back to us when a user taps that button in the keyboard options. Other parameters include `url`, `web_app` and others. Please refer to the reference [here](../reference/objects/gen/inlinekeyboard.md) for more information.
To render out or keyboard, we use the `keyboard()` method. It will output a list representation of the keyboard.
```python
kb.keyboard()
```
Now we can send this keyboard of options to the user. Let's try.
```python
from autotelegram.telegram.context import Context
from autotelegram.telegram.application import PollingApp
from autotelegram.telegram.objects import InlineKeyboardMarkup as keyboard

TOKEN = "token-for-the-bot"

ctx = Context(TOKEN)
app = PollingApp(ctx)

kb = keyboard("stack")
kb.add_button("minor",callback_data = "min")
kb.add_button("moderate",callback_data = "mod")
kb.add_button("major",callback_data = "maj")
kb.add_button("severe",callback_data = "sev")
kb_rep = kb.keyboard()

async def main (update,ctx):
    message = update.message
    text = "Thanks for contacting health-line, could you rate your pain? "
    await message.respond_with_text(text,reply_markup = kb_rep)
    
if __name__ == "__main__":
    app.run(main)
```
So our user will receive a message along with a keyboard of options asking them to rate their pain.

#### Receiving data from Inline keyboard
If we sent `callback_data` along with the keyboard, we shall receive a `CallbackQuery` object once the user taps one of the button options. The `CallbackQuery` contains the data that we sent earlier so we can identify which button the user pressed. More on the `CallbackQuery` object [here](../reference/objects/gen/callbackquery.md).
We can extend the bot to respond to the user after they've tapped on one of our buttons.
```python
from autotelegram.telegram.context import Context
from autotelegram.telegram.application import PollingApp
from autotelegram.telegram.objects import InlineKeyboardMarkup as keyboard

TOKEN = "token-for-the-bot"

ctx = Context(TOKEN)
app = PollingApp(ctx)

kb = keyboard("stack")
kb.add_button("minor",callback_data = "min")
kb.add_button("moderate",callback_data = "mod")
kb.add_button("major",callback_data = "maj")
kb.add_button("severe",callback_data = "sev")
kb_rep = kb.keyboard()

async def main (update,ctx):
    typ,obj = update.get_object()
    if typ == "message":
        text = "Thanks for contacting health-line, could you rate your pain?"
        await obj.respond_with_text(text,reply_markup = kb_rep)
    elif typ == "callback_query":
        match obj.data:
            case "min":
                await obj.answer(text = "your case is mild")
            case "mod":
                await obj.answer(text = "your case is moderate")
            case "maj":
                await obj.answer(text = "your case is major")
            case "sev":
                await obj.answer(text = "your case is severe")
    
if __name__ == "__main__":
    app.run(main)
```
This will respond with a noification to the user telling them "your case is *"
### conclusion
That is a brief on how to work with messages using autotelegram. For more details, browse through the rest of the documenation.