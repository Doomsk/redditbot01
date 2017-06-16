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


def start(bot, update):
    usrnm = (update.message.from_user.first_name).split(' ')[0 if update.message.from_user.first_name[0] != ' ' else 1]
    msgg = u'E aí, ' + usrnm + u'!'
    bot.sendMessage(update.message.chat_id, text=msgg)

def geralista(sbrdt):
    listarddt = []
    for subs in reddit.subreddit(sbrdt).hot():
        if vars(subs)['ups'] >= 5000:
            ups = str(vars(subs)['ups'])
            subreddit = str(vars(subs)['subreddit'])
            titulorddt = (vars(subs)['title'] if len(vars(subs)['title']) <= 110 else vars(subs)['title'][:108] + '...')
            commentrddt = '[Comments](https://www.reddit.com' + vars(subs)['permalink'] + ')'
            linkrddt = '[Link]('+ vars(subs)['url'] + ')'
            listarddt.append((ups, subreddit, titulorddt, commentrddt, linkrddt))
    return listarddt

def selectsubreddits(bot, update, subrddts):
    listarddt = []
    if ";" in subrddts:
        for wordkeysbrddt in subrddts.split(";"):
            try:
                sub1 = reddit.subreddit(wordkeysbrddt)
                print(sub1.fullname)
            except Exception:
                msgg = u"Esse subreddit " + wordkeysbrddt + u" não existe! (eu acho)\n" \
                                                            u"Dá uma conferida se todos estão certos antes de mandar de novo >:)"
                bot.sendMessage(update.message.chat_id, text=msgg)

            else:
                listarddt.append(geralista(wordkeysbrddt))
    else:
        try:
            sub1 = reddit.subreddit(subrddts)
            print(sub1.fullname)
        except Exception:
            msgg = u"Esse subreddit " + subrddts + u" não existe! (eu acho)\n" \
                                                        u"Dá uma conferida se todos estão certos antes de mandar de novo >:)"
            bot.sendMessage(update.message.chat_id, text=msgg)
        else:
            listarddt.append(geralista(subrddts))
    return listarddt


def nadaprafazer(bot, update):
    listarddt = selectsubreddits(bot=bot, update=update, subrddts=update.message.text)
    msgg = u'Aqui vai a lista!\n'
    for ups, subreddit, titulo, comments, link in listarddt:
        msgg += ups + '|' + subreddit + '|' + titulo + '\n|Comments: ' + comments + '|Link: ' + link + '\n-----\n'
    bot.sendMessage(update.message.chat_id, text=msgg, parse_mode=telegram.ParseMode.MARKDOWN)

def main():
    updater = Updater(Config.tokenbot)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("NadaPraFazer", nadaprafazer))
    #dp.add_handler(MessageHandler([Filters.text], testezinho))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    reddit = praw.Reddit(user_agent = 'redditbotthread')
    main()