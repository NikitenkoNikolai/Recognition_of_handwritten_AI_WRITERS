import telebot
import pytesseract
import os
from telebot import types

dir = r'C:/Users/huaweii/PycharmProjects/pythonProject/'

class Bot:

    CHECK_START = False
    BOT_TOKEN = '7000226866:AAG0YNBBOV0i4xI4hKhLrjLSgWGuHaYglEU'
    bot = telebot.TeleBot(BOT_TOKEN)

    @staticmethod
    @bot.message_handler(content_types=['photo'])
    def print_text_from_photo(message):
        if Bot.CHECK_START:
            chat_id = message.chat.id
            img_path = Bot.bot.get_file(message.photo[-1].file_id)

            downloaded_file = Bot.bot.download_file(img_path.file_path)

            src = dir + img_path.file_path.split('/')[-1]
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            text = pytesseract.image_to_string(src, lang='rus')

            Bot.bot.send_message(chat_id, f'Мне кажется, на этом изображении написано: {text}')
            os.remove(src)
        else:
            Bot.bot.send_message(message.chat.id, 'Вы забыли запустить бота :)')


    @bot.message_handler(commands=['start'])
    def start_message(message):
        Bot.CHECK_START = True
        chat_id = message.chat.id
        markup = types.InlineKeyboardMarkup()
        button_start = types.InlineKeyboardButton('Распознать текст с изображения', callback_data='work')
        markup.add(button_start)
        Bot.bot.send_message(chat_id, f'Чего желаете, {message.from_user.first_name}?', reply_markup=markup)

    @bot.message_handler()
    def process_photo_message(message):
        try:
            raise TypeError('Это не изображение, попробуйте снова!')
        except TypeError as e:
            Bot.bot.send_message(message.chat.id, e)

    @bot.callback_query_handler(func=lambda callback: True)
    def print_steps(callback):
        chat_id = callback.message.chat.id
        if callback.data == 'work':
            Bot.bot.reply_to(callback.message, 'Загрузите изображение:')
            Bot.bot.delete_message(chat_id, callback.message.message_id)

Bot.bot.infinity_polling()