> work-in-progress

Autotelegram is composed of:
- Telegram body
- Network system

### Telegram body
The telegram body contains all telegram specific modules. They are located in the `telegram` modules.
We can break them down into
- objects
- methods
- parser
- application
- context

#### objects
Telegram objects are our python representation of the JSON data that we send and receive from telegram bots. The telegram bot api page refers to them as types and gives detailed description of each of them. You can check the complete list [here](https://core.telegram.org/bots/api#available-types).
We divide objects into **general purpose** and **special purpose** objects. The general purpose objects live in the `autotelegram/telegram/objects` module while special purpose objects live in the `autotelegram/telegram/objects/<special-purpose>` module. For example, a special purpose object like **sticker** is located in `autotelegram/telegram/objects/stickers`
