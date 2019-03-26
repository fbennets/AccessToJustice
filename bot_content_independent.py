# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from bot_data import *
import logging
from credentials_test import *




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
#  Moegliche States werden definiert
START, CHOICE, CHECK_ANSWER, END = range(4)

def start(bot, update, chat_data):
    reply_keyboard = [data['start']['answers']]

    update.message.reply_text(
        data['start']['question'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    chat_data['last_node'] = 'start'

    return CHECK_ANSWER


def question(bot, update, chat_data, step):
    reply_keyboard = [data[step]['answers']]
    update.message.reply_text(
        data[step]['question'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    chat_data['last_node'] = step
    return CHECK_ANSWER


def check_answer (bot, update, chat_data):
    answer_given = update.message.text.encode('ascii', 'ignore')
    step = data[chat_data['last_node']]['rules'][answer_given]
    question (bot,update, chat_data, step)

def end (bot, update, chat_data):
    update.message.reply_text('Danke, dass du den Bot benutzt hast! Schreibe /cancel um neuzustarten')



# Check if entered value is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token2)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_chat_data=True)],

        states={


            CHECK_ANSWER: [MessageHandler(Filters.text, check_answer, pass_chat_data=True)],



        },

        fallbacks=[CommandHandler('cancel', start, pass_chat_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
