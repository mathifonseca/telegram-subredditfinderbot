import sys
import telepot
import re

TOKEN = sys.argv[1]
AUTHOR = sys.argv[2]
REDDIT_URL = 'https://reddit.com'


def on_chat(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    print(msg)

    reply = 'What?'

    try:
        if content_type == 'text':
            txt = msg['text']
            if txt:
                if txt.startswith('/r '):
                    parts = txt.split()
                    if len(parts) != 2:
                        reply = 'Send me a subreddit'
                    else:
                        reply = format_url(parts[1])
                elif re.match(r'^/r/\w+$', txt):
                    reply = format_url(txt)
                else:
                    reply = '%s, tu vieja' % txt

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


bot = telepot.Bot(TOKEN)
bot.message_loop(on_chat, run_forever='Listening...')