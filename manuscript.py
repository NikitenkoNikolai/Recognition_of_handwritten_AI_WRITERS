import telebot
from telebot import types
import time
import shutil
from translate import Translator

class Bot:

    CHECK_START = False
    LANGUAGE_MODEL = None
    FOLDER_PATH = '/content/drive/MyDrive/manuscript_bot/word'
    TEST_IMAGE_PATH = '/content/drive/MyDrive/manuscript_bot/test_image.jpg'
    BOT_TOKEN = '7000226866:AAG0YNBBOV0i4xI4hKhLrjLSgWGuHaYglEU'
    bot = telebot.TeleBot(BOT_TOKEN)

    @bot.message_handler(content_types=['photo'])
    def print_text_from_photo(message):
        global message_img
        message_img = message
        chat_id = message.chat.id

        if Bot.CHECK_START:
            if Bot.LANGUAGE_MODEL is None:
                Bot.bot.send_message(message.chat.id, message_list[15])
            else:

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

    @bot.message_handler(commands=['settings'])
    def settings(message):
        chat_id = message.chat.id

        keyboard = types.InlineKeyboardMarkup()
        BUTTON_RUSSIAN = types.InlineKeyboardButton(message_list[12], callback_data='russian')
        BUTTON_ENGLISH = types.InlineKeyboardButton(message_list[13], callback_data='english')

        keyboard.row(BUTTON_RUSSIAN, BUTTON_ENGLISH)

        Bot.bot.send_message(chat_id, message_list[14], reply_markup=keyboard, parse_mode='html')

    @bot.callback_query_handler(func=lambda callback: True)
    def print_steps(callback):
        dict_callfunction = {
            'start': Bot.next_step,
            'get_img': Bot.get_test_image,
            'translate': Bot.print_text(True),
            'continue': Bot.print_text(),
            'russian': Bot.choose_language('rus'),
            'english': Bot.choose_language('eng')
                    }

        dict_callfunction[callback.data](callback.message)

    @bot.message_handler(commands=['test_image'])
    def get_test_image(message):
        chat_id = message.chat.id
        with open(Bot.TEST_IMAGE_PATH, 'rb') as image_file:
            img = image_file.read()
        Bot.bot.send_document(chat_id, img, reply_to_message_id=message.message_id, visible_file_name='test_image.jpg')

    @staticmethod
    def choose_language(language):
        def answer(message):
          Bot.LANGUAGE_MODEL = language
          if Bot.LANGUAGE_MODEL == 'rus':
              Bot.bot.send_message(message.chat.id, f'Выбран {message_list[12]} язык.')
          else:
              Bot.bot.send_message(message.chat.id, f'Выбран {message_list[13]} язык')
          Bot.bot.delete_message(message.chat.id, message.message_id)
        return answer

    @staticmethod
    def text_difinition(message, translate=False):
        img_path = Bot.bot.get_file(message.photo[-1].file_id)
        downloaded_file = Bot.bot.download_file(img_path.file_path)

        src = '/content/drive/MyDrive/manuscript_bot/' + img_path.file_path.split('/')[-1]
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        module = Manuscript(src, Bot.FOLDER_PATH, model_rus if Bot.LANGUAGE_MODEL == 'rus' else model_eng)
        text = module.process_and_predict()

        os.remove(src)
        shutil.rmtree(Bot.FOLDER_PATH)

        if translate:
            if Bot.LANGUAGE_MODEL == 'rus':
                translator = Translator(from_lang='ru', to_lang='en')
                text = translator.translate(text)
            elif Bot.LANGUAGE_MODEL == 'eng':
                translator = Translator(from_lang='en', to_lang='ru')
                text = translator.translate(text)
            else:
                text = 'Не поддерживаемый язык для перевода.'
        return text


    @staticmethod
    def print_text(translate=False):
        def func(message):
            chat_id = message.chat.id
            text = Bot.text_difinition(message_img, translate)
            Bot.bot.send_message(chat_id, f'{message_list[1]}\n\n<blockquote>{text}</blockquote>', parse_mode='html')
            Bot.bot.delete_message(chat_id, message.message_id)
        return func

    @staticmethod
    def next_step(message):
        Bot.CHECK_START = True
        chat_id = message.chat.id
        Bot.bot.send_message(chat_id, message_list[5], parse_mode='html')
        Bot.bot.delete_message(chat_id, message.message_id)

    @bot.message_handler()
    def text_from_user(message):
        try:
            raise TypeError(message_list[7])
        except TypeError as e:
            Bot.bot.send_message(message.chat.id, e)

Bot.bot.infinity_polling()
