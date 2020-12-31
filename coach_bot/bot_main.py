import telebot
from telebot.types import Message
from config.config import TOKEN, ADMIN_ID
from db import storage

bot = telebot.TeleBot(TOKEN, threaded=False)
storage = storage.MongodbService.get_instance()
users = set([x['_id'] for x in storage.get_data_users()])
chats = set([x['_id'] for x in storage.get_data_chats()])


@bot.message_handler(commands=['start', 'stop'])
def command_handler(message: Message):
    text_ru = ''
    text_en = ''
    if message.html_text == '/start':
        if not message.chat.id in chats:
            storage.save_chat(message.chat.id)
        if not message.chat.id in users:
            storage.save_user(message.from_user.id)
        text_ru = f"Рад тебя видеть, {message.from_user.first_name} =)"
        text_en = f"I'm glad to see you, {message.from_user.first_name} =)"
    elif message.html_text == '/stop':
        text_en = "That's pity. Bye!"
        text_ru = 'Жаль, до свидания!'
        chats.discard(message.chat.id)
        storage.remove_chat(message.chat.id)

    if message.from_user.language_code == 'en':
        bot.reply_to(message, f"{text_en}")
    else:
        bot.reply_to(message, f"{text_ru}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID and
                        message.text == "TOTAL_USERS",
                     content_types=['text'])
def repost_to_all(message):
    bot.send_message(ADMIN_ID, f"""{len(storage.get_data_users())}""")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['text'])
def repost_to_all(message):
    for chat_id in storage.get_data_chats():
        bot.send_message(chat_id['_id'],
                         f"""{message.__dict__[message.content_type]}""")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['sticker'])
def repost_to_all_sticker(message):
    for chat_id in storage.get_data_chats():
        bot.send_sticker(chat_id['_id'],
                         f"""{message.__dict__[message.content_type].file_id}""")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['voice'])
def repost_to_all_(message):
    for chat_id in storage.get_data_chats():
        bot.send_voice(chat_id['_id'],
                         f"{message.__dict__[message.content_type].file_id}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['photo'])
def repost_to_all(message):
    for chat_id in storage.get_data_chats():
        bot.send_photo(chat_id['_id'],
                         f"{message.__dict__[message.content_type].file_id}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['video'])
def repost_to_all(message):
    for chat_id in storage.get_data_chats():
        bot.send_video(chat_id['_id'],
                         f"{message.__dict__[message.content_type].file_id}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['location'])
def repost_to_all(message):
    for chat_id in storage.get_data_chats():
        bot.send_location(chat_id['_id'],
                         f"{message.__dict__[message.content_type].file_id}")


@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID,
                     content_types=['document'])
def repost_to_all(message):
    for chat_id in storage.get_data_chats():
        bot.send_document(chat_id['_id'],
                         f"{message.__dict__[message.content_type].file_id}")


@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID,
                content_types=['audio', 'photo', 'voice', 'video', 'document',
                                    'text', 'location', 'contact', 'sticker'])
def repost_to_all(message):
    bot.send_message(message.chat.id, 'Я пока не научился отвечать вам')


bot.infinity_polling()
