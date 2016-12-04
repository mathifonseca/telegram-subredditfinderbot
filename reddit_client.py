import config
import praw

CLIENT_ID = config.load_config('REDDIT_CLIENT_ID', 3)
CLIENT_SECRET = config.load_config('REDDIT_CLIENT_SECRET', 4)
USER_AGENT = config.load_config('REDDIT_USER_AGENT', 5)

reddit = praw.Reddit(user_agent=USER_AGENT,
                     client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET)


def search_subreddits(query):
    subs = reddit.subreddits.search_by_name(query)
    return [{
        'name': sub.display_name,
        'title': sub.title,
        'url': sub.url
       } for sub in subs]
