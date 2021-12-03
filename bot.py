#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, MessageFilter, ConversationHandler
from telegram import ReplyKeyboardMarkup
import telebot
from telebot import types

from dados import *
from resources import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    clear_all_resources(update, context)
    clear_results_dados_csv()
    
    keyboard = [['Sí', 'No']]
    context.bot.send_message(chat_id=update.message.chat.id,
                     text="""Buenas! Sale un Catán?\nPara ver los comandos disponibles escribí /help cuando quieras.\n\nQuerés cargar los números de cada recurso?""",
                     reply_markup=ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True,
                                       ),
                     parse_mode='HTML')

    return FILL_OR_NOT


# def help(update, context):


def invalid(update, context):
    """ Cancel current conversation """
    update.message.reply_text(
        """Please enter a valid dice result.\nIf you want to start again type /start.""")
    return ConversationHandler.END


class FilterDadosResults(MessageFilter):
    def filter(self, message):
        return message.text in [str(res) for res in list(range(1, 13))]

# Remember to initialize the class.
filter_dados_results = FilterDadosResults()


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("2120082459:AAFjuAwfrd85FvxigvlsRmNcECTuMXR18Lk", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    # dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            fallbacks=[MessageHandler(Filters.text, invalid)],

            states={
                FILL_OR_NOT: [MessageHandler(Filters.regex('^(Sí|S)$'), fill_wood), MessageHandler(Filters.regex('^(No|N)$'), process_dados)], 
                FILL_WOOD: [MessageHandler(Filters.regex('^(Sí|S)$') | filter_dados_results, fill_wood), MessageHandler(Filters.regex('^(Terminar madera)$'), fill_clay)], 
                FILL_CLAY: [MessageHandler(filter_dados_results, fill_clay), MessageHandler(Filters.regex('^(Terminar arcilla)$'), fill_sheep)],
                FILL_SHEEP: [MessageHandler(filter_dados_results, fill_sheep), MessageHandler(Filters.regex('^(Terminar ovejas)$'), fill_wheat)],
                FILL_WHEAT: [MessageHandler(filter_dados_results, fill_wheat), MessageHandler(Filters.regex('^(Terminar trigo)$'), fill_rock)],
                FILL_ROCK: [MessageHandler(filter_dados_results, fill_rock), MessageHandler(Filters.regex('^(Terminar piedra)$'), process_dados)],
                DADOS: [MessageHandler(Filters.regex('^(No|N)$') | filter_dados_results, process_dados)]
            },

            
        )
        
    dp.add_handler(conv_handler)
    # dp.add_handler(MessageHandler(Filters.text & filter_dados_results, process_dados))

    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()