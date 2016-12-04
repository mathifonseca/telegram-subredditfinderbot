import config
import reddit_client
import telepot
import re
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent


def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', msg)

        try:
            query_results = search_subreddits(msg['query'])

            if len(query_results) == 0:
                articles = [InlineQueryResultArticle(
                                id=query_string,
                                title=query_string,
                                input_message_content=InputTextMessageContent(
                                    message_text=format_url(query_string)
                                )
                            )]
            else:
                articles = [InlineQueryResultArticle(
                                id=sub['url'],
                                title='%s - %s' % (sub['name'], sub['title']),
                                input_message_content=InputTextMessageContent(
                                    message_text=format_url(sub['url'])
                                )
                            ) for sub in query_results]

            return articles
        except Exception as ex:
            print ex
            bot.sendMessage(AUTHOR, 'ERROR! %s' % ex)

    if msg['query']:
        answerer.answer(msg, compute)


def on_chosen_inline_result(msg):
    print ('Inline Result:', msg)


def on_chat(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', msg)
    reply = 'What?'

    try:
        if content_type == 'text':
            txt = msg['text']
            if txt:
                if re.match(r'^/r/\w+$', txt):
                    reply = format_url(txt)
                elif txt.startswith('/'):
                    command = txt.split()
                    if len(command) != 2:
                        reply = 'Send me a subreddit name!'
                    else:
                        if command[0] == '/r':
                            reply = format_url(command[1])
                        elif command[0] == '/search':
                            reply = search_subreddits(command[1], True)
                else:
                    reply = '%s, tu vieja' % txt

        if reply:
            bot.sendMessage(chat_id, reply)
    except Exception as ex:
        print ex
        bot.sendMessage(AUTHOR, 'ERROR! %s' % ex)


def format_url(sub):
    url = REDDIT_URL
    if sub.startswith('/r/'):
        url += sub
    else:
        url += '/r/%s' % sub
    return url


def search_subreddits(query, string=False):
    results = reddit_client.search_subreddits(query)
    if string:
        subs = ''
        if len(results) == 0:
            subs = 'No results :('
        else:
            for sub in results:
                subs += '%s - %s\n' % (sub['name'], format_url(sub['url']))
        return subs
    else:
        return results


TOKEN = config.load_config('TOKEN')
AUTHOR = config.load_config('AUTHOR', 2)
REDDIT_URL = 'https://reddit.com'

bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)

bot.message_loop({'chat': on_chat,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result},
                 run_forever='Listening...')
