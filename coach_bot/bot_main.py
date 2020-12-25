import telebot
from telebot.types import Message
from coach_bot.config.config import TOKEN, ADMIN_ID
from coach_bot.db import storage

bot = telebot.TeleBot(TOKEN, threaded=False)
storage = storage.MongodbService.get_instance()


@bot.message_handler(commands=['start', 'stop'])
def command_handler(message: Message):
    text_ru = ''
    text_en = ''
    dto = {
        "chat_id": message.chat.id,
        "user_id": message.from_user.id
    }
    if message.html_text == '/start':
        storage.save_chat(message.chat.id)
        storage.save_user(message.from_user.id)
        text_ru = f"Рад тебя видеть, {message.from_user.first_name} =)"
        text_en = f"I'm glad to see you, {message.from_user.first_name} =)"
    elif message.html_text == '/stop':
        text_en = "That's pity. Bye!"
        text_ru = 'Жаль, до свидания!'
        storage.remove_chat(message.chat.id)

    if message.from_user.language_code == 'en':
        bot.reply_to(message, f"{text_en} \n {chat_ids} \n  {message}")
    else:
        bot.reply_to(message, f"{text_ru}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['text'])
def repost_to_all(message):  # Название функции не играет никакой роли
    for chat_id in storage.get_data_chats():
        bot.send_message(chat_id['_id'],
                         f"""{message.__dict__[message.content_type]}""")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['sticker'])
def repost_to_all_sticker(message):  # Название функции не играет никакой роли
    for chat_id in storage.get_data_chats():
        bot.send_sticker(chat_id['_id'],
                         f"""{message.__dict__[message.content_type].file_id}""")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['voice'])
def repost_to_all_(message):  # Название функции не играет никакой роли
    for chat_id in storage.get_data_chats():
        bot.send_voice(chat_id['_id'],
                         f"{message.__dict__[message.content_type].file_id}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['photo'])
def repost_to_all(message):  # Название функции не играет никакой роли
    for chat_id in storage.get_data_chats():
        bot.send_photo(chat_id['_id'],
                         f"{message.__dict__[message.content_type].file_id}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['video'])
def repost_to_all(message):  # Название функции не играет никакой роли
    for chat_id in storage.get_data_chats():
        bot.send_video(chat_id['_id'],
                         f"{message.__dict__[message.content_type].file_id}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['location'])
def repost_to_all(message):  # Название функции не играет никакой роли
    for chat_id in storage.get_data_chats():
        bot.send_location(chat_id['_id'],
                         f"{message.__dict__[message.content_type].file_id}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['document'])
def repost_to_all(message):  # Название функции не играет никакой роли
    for chat_id in storage.get_data_chats():
        bot.send_document(chat_id['_id'],
                         f"{message.__dict__[message.content_type].file_id}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID and
                        message.text == "All_chats",
                     content_types=['text'])
def repost_to_all(message):  # Название функции не играет никакой роли
    for chat_id in chat_ids:
        bot.send_message(chat_id, f"""{users_id}""")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли
    bot.send_message(message.chat.id, f'{message.text} \n {message} ')


bot.infinity_polling()
