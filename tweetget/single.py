import json
import datetime
import os

from twython import Twython
from .settings import DATA_PATH, TWITTER_API_KEY, TWITTER_API_SECRET, QUERY


def get_twitter():
    twitter = Twython(TWITTER_API_KEY, TWITTER_API_SECRET, oauth_version=2)
    return Twython(TWITTER_API_KEY, access_token=twitter.obtain_access_token())


def get_tweets(twitter=None, oldest_id=None, query=None):
    query = query or QUERY
    twitter = twitter or get_twitter()

    params = {
        'q': QUERY,
        'lang': 'en',
        'count': '100',
        'result_type': 'recent'
    }

    if oldest_id:
        params['max_id'] = oldest_id

    try:
	resp = twitter.search(**params)
    except:
	print(twitter._last_call)
        raise

    return resp['statuses']


def save_tweets(tweets, query=None):
    query = query or QUERY
    query = query.split()[0]
    now = datetime.datetime.utcnow()
    filename = os.path.join(DATA_PATH, '{}-{}.json'.format(query, now.isoformat()).replace(':', '_'))
    with open(filename, 'a') as f:
        f.write(json.dumps(tweets, indent=2))

    print('{} tweets written to {}'.format(len(tweets), filename))


if __name__ == '__main__':
    twitter = get_twitter()
    tweets = get_tweets(twitter)
    save_tweets(tweets)
