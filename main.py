import praw
import logging
from telegram.ext import Updater, CommandHandler
from configs import Config


def start(bot, update):
    usrnm = (update.message.from_user.first_name).split(' ')[0 if update.message.from_user.first_name[0] != ' ' else 1]
    msgg = u'E aí, ' + usrnm + u'! Dá um /nadaprafazer <subreddit> e procure pelas hot threads do reddit! :>'
    bot.sendMessage(update.message.chat_id, text=msgg)


def selectsubreddits(bot, update, subrddts):
    contadorzinho = 0
    sbrddtsfora = []
    listarddt = []
    valid = False
    msgg = u'Pesquisando! Só um momento... :d'
    bot.sendMessage(update.message.chat_id, text=msgg)
    if ";" in subrddts:
        for wordkeysbrddt in subrddts.split(";"):
            try:
                sub1 = reddit.subreddit(wordkeysbrddt)
                print(sub1.fullname)
            except Exception:
                valid = False
                listarddt = []
                listarddt.append(wordkeysbrddt)

            else:
                for subs in reddit.subreddit(wordkeysbrddt).hot():
                    if vars(subs)['ups'] >= 5000:
                        ups = str(vars(subs)['ups'])
                        subreddit = str(vars(subs)['subreddit'])
                        titulorddt = (vars(subs)['title'] if len(vars(subs)['title']) <= 110 else vars(subs)['title'][:108] + '...')
                        commentrddt = 'redd.it/' + vars(subs)['name'].split('_')[1]
                        linkrddt = '' + vars(subs)['url']
                        print(ups + subreddit + commentrddt)
                        listarddt.append(ups + ' | ' + subreddit + ' | ' + titulorddt + '\n|Comments: ' + commentrddt + ' |Link: ' + linkrddt)
                        valid = True
                        contadorzinho += 1
                if contadorzinho == 0:
                    sbrddtsfora.append(wordkeysbrddt)
                else:
                    contadorzinho = 0

    else:
        try:
            sub1 = reddit.subreddit(subrddts)
            print(sub1.fullname)
        except Exception:
            valid = False
            listarddt = []
            listarddt.append(subrddts)
        else:
            for subs in reddit.subreddit(subrddts).hot():
                if vars(subs)['ups'] >= 5000:
                    ups = str(vars(subs)['ups'])
                    subreddit = str(vars(subs)['subreddit'])
                    titulorddt = (vars(subs)['title'] if len(vars(subs)['title']) <= 110 else vars(subs)['title'][:108] + '...')
                    commentrddt = 'redd.it/' + vars(subs)['name'].split('_')[1]
                    linkrddt = '' + vars(subs)['url']
                    print(ups + subreddit + commentrddt)
                    listarddt.append(ups + ' | ' + subreddit + ' | ' + titulorddt + '\n|Comments: ' + commentrddt + ' |Link: ' + linkrddt)
                    valid = True
                    contadorzinho += 1
            if contadorzinho == 0:
                sbrddtsfora.append(subrddts)
            else:
                contadorzinho = 0
    return listarddt, valid, sbrddtsfora


def nadaprafazer(bot, update):
    msgsbrddts = (update.message.text).split()
    print(update.message.text)
    print(msgsbrddts)
    if len(msgsbrddts) > 1:
        if msgsbrddts[1] == '':
            msgg = u'Precisa enviar algo para eu pesquisar! :('
            bot.sendMessage(update.message.chat_id, text=msgg)
        else:
            listarddt, valid, subdefora = selectsubreddits(bot=bot, update=update, subrddts=msgsbrddts[1])
            if not valid:
                msgg = u'' \
                       u'Pelo menos um subreddit, tipo esse ' + listarddt[0] + u', não existe! (eu acho)\n' \
                                                          u'Dá uma conferida se todos estão certos antes de mandar de novo >:)'
            else:
                print(len(listarddt))
                msgg = u'Pronto! Aqui vai a lista:\n\n'
                for itenslista in listarddt:
                    msgg += itenslista + '\n-----\n'
                if len(subdefora) > 0:
                    msgg += u'Até estão os resultados, mas não houve nenhuma ' \
                            u'thread com mais de 5000 para esse' + ('s' if len(subdefora) > 1 else '') + ' aqui : ' + ' '.join(subdefora)
            bot.sendMessage(update.message.chat_id, text=msgg)
    else:
        msgg = u'Precisa enviar algo para eu pesquisar! :('
        bot.sendMessage(update.message.chat_id, text=msgg)

def main():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger = logging.getLogger('prawcore')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    updater = Updater(Config.tokenbot)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("nadaprafazer", nadaprafazer))
    dp.add_handler(CommandHandler("NadaPraFazer", nadaprafazer))
    #dp.add_handler(MessageHandler([Filters.text], testezinho))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    reddit = praw.Reddit('redditbot01', user_agent = 'redditbotthread')
    main()