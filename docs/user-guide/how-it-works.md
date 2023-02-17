
### Overview
Here's an overview of how autotelegram works.
The telegram http based API as provided by telegram is mainly composed of two parts:
the **telegram objects** and the **telegram methods**.
The telegram objects include objects like `Message` object, `Update` object, `User` object, `Chat` object and many others. They are represented by telegram in JSON form. for example, below is a response of a telegram bot with an update object
```JSON
{"ok":true,
"result":[
    {"update_id":184545088,
    "message":{
        "message_id":156,
        "from":{
            "id":910177620,
            "is_bot":false,
            "first_name":"TobiasHT \ud83c\uddfa\ud83c\uddec",
            "language_code":"en"
            },
            "chat":{
                "id":910177620,
                "first_name":"TobiasHT \ud83c\uddfa\ud83c\uddec",
                "type":"private"
                },
                "date":1676294169,
                "text":"Hi"
            }
        }
    ]
}
```
after making a request to get updates, telegram responds with a JSON object with the first element being `ok`. if `ok` is `true`, then our request was sucessful and we receive our updates as a list of `result`s. If `ok` is `false`, then there was something wrong with our request and telegram returns to us an `error code` and `description` of the error that occured.
You can read more about error handling [here](https://core.telegram.org/api/errors).
Autotelegram automatically intercepts this error for you and raises it as a python error called `TelegramResultError` which you can catch in your programs

#### constructing the object tree
Working with JSON data in this form is really tedious. It takes a lot of effort to query deeply nested elements and attributes. And if you look at the example response above closely, you can actually see that the result builds out as a tree of telegram objects with update being the root object and the other objects following as children and children of children. Autotelegram takes the initiative to transform this JSON data into a python telegram object tree that you can easily work with in your code. On every response from a telegram bot, autotelegram returns this object tree for you.
You can then easily extract the object of your choice and interact with it. For example, working with an Update object would be as easy as:
```python
>>> update = bot.get_updates()[0]
>>> update.message
<class 'autotelegram.telegram.objects.message.Message'>
>>> msg = _
>>> msg.text
"Hi"
>>> update.update_id
184545088
```
This is just a crude representation of how you would interact with the update object and the rest of the objects. You can access deeply nested attributes easily, such as;
```python
>>> chat_id = update.message.chat.id
>>> chat_id
910177620
```
### conclusion
Next, let's see how we can actually make requests to the telegram bot and interact with it.