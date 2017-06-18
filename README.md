# Killlbot
Killl vem de Komandointeligentelalala. Ele era um bot de mIRC com comandos bugados e desinteligência artificial.



Este será (um dia) o maior bot do telegram, para honrar seu legado deixado no mIRC. Mas, por enquanto, ele vai servir para testar algumas funcionalidades :)

## Reddit threads 5000+

<p>Essa função retorna todos os hot threads dos desejados subreddits pelo comando <b><i>/nadaprafazer</i></b>. 
Exemplo:</p>

<code><b>/nadaprafazer</b> cheese;physics</code>

<p>Ele retorna os hot threads (que possuírem 5000+ pontos) com as seguintes informações:</p>

<p>pontos|subreddit|título<br>
|Comments: link<br>
|Link da thread: link</p>


------------------------
## Informações relevantes

<p>Caso esteja afim de dar um fork, precisará realizar algumas tarefas:</p>
<p>1. Criar um arquivo praw.ini com as seguintes especificações: <br>
<pre><code>[DEFAULT]
# A boolean to indicate whether or not to check for package updates.
check_for_updates=True

comment_kind=t1<br>
message_kind=t4<br>
redditor_kind=t2<br>
submission_kind=t3<br>
subreddit_kind=t5<br>

oauth_url=https://oauth.reddit.com

reddit_url=https://www.reddit.com

short_url=https://redd.it

[redditbot01]<br>
username=Username<br>
client_id=Clientid<br>
password=Password<br>
client_secret=ClientSecret<br>
</code></pre></p>

<p>Não esqueça de registrar seu script para adquirir a autentiação do <a href=https://github.com/reddit/reddit/wiki/OAuth2>Reddit<a> para pegar os dados e preenche-los no praw.ini
