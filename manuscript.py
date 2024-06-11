import telebot
import pytesseract
import os
from telebot import types
import time

dir = r'C:/Users/huaweii/PycharmProjects/pythonProject/'

# набор фраз для ответа на сообщение
with open('start.txt', encoding='utf-8') as file:
    # 0: Приветствие;
    # 1: Опознавательный текст;
    # 2: Сообщение о незапущенном боте;
    # 3: Кнопка распознавание текста;
    # 4: Кнопка тестового изображения;
    # 5: Ответ на распознавание текста;
    # 6: Сообщение ожидания;
    # 7: Сообщение о некорректном сообщении.
    message_list = file.read().split('\n\n\n')


class Bot:

    CHECK_START = False
    BOT_TOKEN = '7000226866:AAG0YNBBOV0i4xI4hKhLrjLSgWGuHaYglEU'
    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(content_types=['photo'])
    def print_text_from_photo(message):
        chat_id = message.chat.id

        if Bot.CHECK_START:
            img_path = Bot.bot.get_file(message.photo[-1].file_id)

            downloaded_file = Bot.bot.download_file(img_path.file_path)

            src = dir + img_path.file_path.split('/')[-1]
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            text = pytesseract.image_to_string(src, lang='rus')

            Bot.bot.send_message(chat_id, fr'{message_list[1]} <b>{text}</b>', parse_mode='html')
            os.remove(src)
        else:
            Bot.bot.send_message(chat_id, message_list[2])


    @bot.message_handler(commands=['start'])
    def start_message(message):
        # флаг для запуска бота и разблокировки всех функций
        Bot.CHECK_START = True

        chat_id = message.chat.id
        # кнопки бота
        markup = types.InlineKeyboardMarkup()
        button_text = types.InlineKeyboardButton(message_list[3], callback_data='text')
        button_test_image = types.InlineKeyboardButton(message_list[4], callback_data='get_img')
        markup.add(button_text)
        markup.add(button_test_image)
        Bot.bot.send_message(chat_id, message_list[0], reply_markup=markup)

    @bot.callback_query_handler(func=lambda callback: True)
    def print_steps(callback):
        chat_id = callback.message.chat.id
        if callback.data == 'text':
            Bot.bot.send_message(chat_id, message_list[5])
            time.sleep(1)
            Bot.bot.reply_to(callback.message, message_list[6])
        elif callback.data == 'get_img':
            Bot.get_test_image(callback.message)

    @bot.message_handler(commands=['help'])
    def help_message(message):
        Bot.bot.send_message(message.chat.id, 'Когда будем смотреть фильм ужасов?')

    @bot.message_handler(commands=['test_image'])
    def get_test_image(message):
        chat_id = message.chat.id
        with open('test_image.jpg', 'rb') as image_file:
            img = image_file.read()
        time.sleep(0.5)
        Bot.bot.send_document(chat_id, img, reply_to_message_id=message.message_id, visible_file_name='test_image.jpg')

    @bot.message_handler()
    def text_from_user(message):
        # перехватываем всё, что не является изображением и возбуждаем исключение
        try:
            raise TypeError(message_list[7])
        except TypeError as e:
            Bot.bot.send_message(message.chat.id, e)

Bot.bot.infinity_polling()
