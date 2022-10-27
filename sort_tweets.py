import html
import sys
import json
import random
import subprocess
from dateutil.parser import parse


def read_json():
    if len(sys.argv) != 3:
        sys.exit('Usage: python3 sort_tweets.py [tweet.js] [output_file.txt]')
    with open(sys.argv[1], 'r') as file:
        _data = file.read()
        return _data[25:len(_data)]


def is_valid(_tweet):
    _tweet = _tweet['tweet']
    if _tweet['retweeted']:
        return False
    if 'in_reply_to_screen_name' in _tweet:
        return False
    if _tweet['full_text'].startswith('RT @'):
        return False
    if len(_tweet['full_text'].split()) < 8:
        return False

    _tweet = _tweet['entities']

    if len(_tweet['urls']) != 0:
        return False
    if 'media' in _tweet:
        return False
    return True


def get_text(_tweet):
    return _tweet['tweet']['full_text']

def get_date(_tweet):
    return _tweet['tweet']['created_at']


if __name__ == '__main__':
    # setup
    output_json_file = open(sys.argv[2], 'w')
    string_data = read_json()
    json_data = json.loads(string_data)
    counter = 0
    tweet_list = []

    for tweet in json_data:
        if is_valid(tweet):
            _text = html.unescape(get_text(tweet))
            _date = get_date(tweet)
            tweet_list.append({"tweet": _text, "date": _date})
            counter += 1

    # sort tweets

    tweet_list.sort(key=lambda x: parse(x["date"]))
    for tweet in tweet_list:
        json.dump({"date": tweet["date"], "tweet": tweet["tweet"]}, output_json_file, separators=(',', ':'))
        output_json_file.write('\n')

    print("Total tweets: " + str(len(json_data)))
    print("Only text tweets: " + str(counter))
    output_json_file.close()
