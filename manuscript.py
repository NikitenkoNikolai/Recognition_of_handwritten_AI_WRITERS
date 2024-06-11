import telebot
from telebot import types
import pytesseract
import os
import time
from translate import Translator
from langid import classify

dir = r'C:/Users/huaweii/PycharmProjects/pythonProject/'

# набор фраз для ответа на сообщение
with open('start.txt', encoding='utf-8') as file:
    # 0: Приветствие;
    # 1: Опознавательный текст;
    # 2: Сообщение о незапущенном боте;
    # 3: Кнопка получения результата;
    # 4: Кнопка тестового изображения;
    # 5: Ответ на распознавание текста;
    # 6: Сообщение ожидания;
    # 7: Сообщение о некорректном сообщении.
    # 8: Стартовое сообщение
    # 9: Кнопка старта
    # 10: Кнопка перевода языка
    # 11: Сообщение об успешном распознавании текста
    message_list = file.read().split('\n\n\n')

class Bot:

    CHECK_START = False
    BOT_TOKEN = '7000226866:AAG0YNBBOV0i4xI4hKhLrjLSgWGuHaYglEU'
    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(content_types=['photo'])
    def print_text_from_photo(message):
        global message_img
        message_img = message
        chat_id = message.chat.id

        if Bot.CHECK_START:
            # кнопки
            keyboard = types.InlineKeyboardMarkup()
            BUTTON_TRANSLATE = types.InlineKeyboardButton(message_list[10], callback_data='translate')
            BUTTON_CONTINUE = types.InlineKeyboardButton(message_list[3], callback_data='continue')
            keyboard.add(BUTTON_CONTINUE)
            keyboard.add(BUTTON_TRANSLATE)

            Bot.bot.send_message(chat_id, message_list[11], reply_markup=keyboard, parse_mode='html')
        else:
            Bot.bot.send_message(chat_id, message_list[2])


    @bot.message_handler(commands=['start'])
    def start_message(message):
        chat_id = message.chat.id
        # кнопки бота
        keyboard = types.InlineKeyboardMarkup()
        BUTTON_START = types.InlineKeyboardButton(message_list[9], callback_data='start')
        BUTTON_TEST_IMAGE = types.InlineKeyboardButton(message_list[4], callback_data='get_img')
        keyboard.add(BUTTON_START)
        keyboard.add(BUTTON_TEST_IMAGE)

        Bot.bot.send_message(chat_id, message_list[8], reply_markup=keyboard, parse_mode='html')

    @bot.callback_query_handler(func=lambda callback: True)
    def print_steps(callback):
        chat_id = callback.message.chat.id
        if callback.data == 'start':
            Bot.next_step(callback.message)
        elif callback.data == 'get_img':
            Bot.get_test_image(callback.message)
        elif callback.data == 'translate':
            text = Bot.text_difinition(message_img, True)
            Bot.bot.send_message(chat_id, text)
            time.sleep(0.35)
            Bot.bot.delete_message(chat_id, callback.message.message_id)
        elif callback.data == 'continue':
            text = Bot.text_difinition(message_img)
            Bot.bot.send_message(chat_id, fr'{message_list[1]} <b>{text}</b>', parse_mode='html')
            time.sleep(0.35)
            Bot.bot.delete_message(chat_id, callback.message.message_id)

    @bot.message_handler(commands=['test_image'])
    def get_test_image(message):
        chat_id = message.chat.id
        with open('test_image.jpg', 'rb') as image_file:
            img = image_file.read()
        time.sleep(0.5)
        Bot.bot.send_document(chat_id, img, reply_to_message_id=message.message_id, visible_file_name='test_image.jpg')

    @staticmethod
    def text_difinition(message, translate=False):
        img_path = Bot.bot.get_file(message.photo[-1].file_id)
        downloaded_file = Bot.bot.download_file(img_path.file_path)

        src = img_path.file_path.split('/')[-1]
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        text = pytesseract.image_to_string(src, lang='rus')
        os.remove(src)

        if translate:
            if classify(text)[0] == 'ru':
                translator = Translator(from_lang='ru', to_lang='en')
                text = translator.translate(text)
            elif classify(text)[0] == 'en':
                translator = Translator(from_lang='en', to_lang='ru')
                text = translator.translate(text)
            else:
                text = 'Не поддерживаемый язык для перевода.'
        return text

    @staticmethod
    def next_step(message):
        Bot.CHECK_START = True
        chat_id = message.chat.id
        Bot.bot.send_message(chat_id, message_list[5], parse_mode='html')
        time.sleep(0.35)
        Bot.bot.delete_message(chat_id, message.message_id)

    @bot.message_handler()
    def text_from_user(message):
        try:
            raise TypeError(message_list[7])
        except TypeError as e:
            Bot.bot.send_message(message.chat.id, e)

Bot.bot.infinity_polling()
