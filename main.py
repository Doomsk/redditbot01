import sys
import platform
import time
import asyncio
import os
import re
import json
import praw
from datetime import datetime
import requests
import telegram
from telegram import LabeledPrice, ShippingOption
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import ParseMode, Message, Chat, InlineKeyboardMarkup, \
    InlineKeyboardButton, ReplyKeyboardMarkup, InlineQueryResultPhoto
from telegram.ext import InlineQueryHandler, ChosenInlineResultHandler, \
    CommandHandler, MessageHandler, Filters, CallbackQueryHandler, \
    PreCheckoutQueryHandler, ShippingQueryHandler
from telegram.ext.dispatcher import run_async
from configs import Config




def main():
    updater = Updater(Config.tokenbot)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler([Filters.text], testezinho))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()