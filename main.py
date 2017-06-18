import re
import logging
import praw
from telegram.ext import Updater, CommandHandler
from configs import Config


def start(bot, update):
    """
    funcao do comando /start
    :param bot: argumento da classe do bot do telegram
    :param update: argumento da classe do ao user/chat
    """
    usrnm = (update.message.from_user.first_name).split(' ')[0 if update.message.from_user.first_name[0] != ' ' else 1]
    msgg = u'E aí, ' + usrnm + u'! Dá um /nadaprafazer <subreddit> e procure pelas hot threads do reddit! :>'
    bot.sendMessage(update.message.chat_id, text=msgg)


def funcsort(tosortlist):
    """
    funcao para realizar a separacao entre o que eh numero e o que nao eh para ordenar de forma decrescente
    :param tosortlist: a lista a ser reordenada
    :return: retorna a lista com numeros e strings, pro argumento key ordenar
    """
    return [int(c) if c.isdigit() else c for c in re.split('(\d+)',tosortlist) ]


def sortingdec(notsortedlist):
    """
    funcao que faz a ordenacao da lista contendo as informacoes do subreddit (ups, subreddit, titulo, comments, link)
    :param notsortedlist: a lista
    :return: lista ordenada decrescentemente
    """
    notsortedlist.sort(key=funcsort, reverse=True)
    return notsortedlist


def selectsubreddits(bot, update, subrddts):
    """
    funcao que lida com a procura pelos hot subreddits que possuam 5000+ pontos (ups)
    organiza em uma lista na forma ups | subreddit | titulo (ate 110 chars, se nao coloca reticencias).
    verifica caso tenha mais de um subreddit procurando pelas ;, se achar, faz o processo pra todos.
    verifica se existe algum subreddit invalido, se existe algum que nao possui nenhum hot 5000+.
    :param bot: argumento da classe do bot do telegram
    :param update: argumento da classe do ao user/chat
    :param subrddts: o(s) subreddit(s) em questao
    :return: uma tupla contendo a lista com as informacoes do subreddit (ups, subreddit, titulo, comments, link),
    uma variavel booleana para saber se houve algum subreddit invalido, 
    uma lista com os subreddits que nao tiveram hot 5000+
    """
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
    """
    funcao do comando /nadaprafazer
    ela verifica se houve algo digitado depois do  comando, chama a funcao selectsubreddits
    pra fazer o trabalho sujo (ler comments da funcao), coloca as mensagens de aviso: se 
    houve algum subreddit invlaido e, se tudo estiver certo, reorganiza a lista dos
    das infos do subreddits pra ficar apresentavel.
    :param bot: argumento da classe do bot do telegram
    :param update: argumento da classe do ao user/chat
    """
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
                newlistarddt = sortingdec(listarddt)
                msgg = u'Pronto! Aqui vai a lista:\n\n'
                for itenslista in newlistarddt:
                    msgg += str(itenslista) + '\n-----\n'
                if len(subdefora) > 0:
                    msgg += u'Aqui estão os resultados, mas não houve nenhuma ' \
                            u'thread com mais de 5000 para esse' + ('s' if len(subdefora) > 1 else '') + ' aqui : ' + ' '.join(subdefora)
            bot.sendMessage(update.message.chat_id, text=msgg)
    else:
        msgg = u'Precisa enviar algo para eu pesquisar! :('
        bot.sendMessage(update.message.chat_id, text=msgg)


def main():
    """
    funcao main() que eh executada com todos as funcoes
    do bot e com um print log para manter um controle
    caso executado no terminal (so pra efeitos de debugging).
    chama o arquivo config.py contendo Config.tokenbot pra 
    pegar os token do bot do telegram.
    """
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
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    """
    coracao do arquivo, chama o Reddit() com os parametros encontrados
    no arquivo praw.ini (pelo redditbot01) e chama o main()
    """
    reddit = praw.Reddit('redditbot01', user_agent = 'redditbotthread')
    main()