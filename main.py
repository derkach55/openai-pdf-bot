import os

import telebot
from dotenv import load_dotenv

from pdf_analysing.analyser import generate_response, analyse_file

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
FILE_TO_ANALYSE = os.environ.get('FILE_TO_ANALYSE')

chain = analyse_file(FILE_TO_ANALYSE)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id,
                         "Welcome to AiBot, write your question and I'll try to answer your question")
    else:
        response = generate_response(message.text, chain)
        bot.send_message(message.from_user.id, response)


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
