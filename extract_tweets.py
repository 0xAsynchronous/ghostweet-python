import html
import sys
import json
import random
import subprocess


def read_json():
    if len(sys.argv) != 3:
        sys.exit('Usage: python3 extract_tweets.py [tweet.js] [output_file.txt]')
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
    if "  " in _tweet['full_text']:
        print(_tweet["full_text"])

    _tweet = _tweet['entities']

    if len(_tweet['urls']) != 0:
        return False
    if 'media' in _tweet:
        return False
    return True


def get_text(_tweet):
    return _tweet['tweet']['full_text']


if __name__ == '__main__':
    # setup
    output_file = open(sys.argv[2], 'w')
    output_json_file = open('data.jsonl', 'w')
    string_data = read_json()
    json_data = json.loads(string_data)
    counter = 0
    tweet_list = []

    for tweet in json_data:
        if is_valid(tweet):
            _text = html.unescape(get_text(tweet))
            output_file.write(_text + '\n\n<--BREAK-->\n\n')
            split_word_count = random.randint(3, 7)
            prompt = " ".join(_text.split()[:split_word_count]) + '#->'
            completion = ' ' + " ".join(_text.split()[split_word_count:]) + '\n'

            json.dump({"prompt": prompt, "completion": completion}, output_json_file, separators=(',', ':'))
            output_json_file.write('\n')

            counter += 1
    print("Total tweets: " + str(len(json_data)))
    print("Only text tweets: " + str(counter))
    output_file.close()
    output_json_file.close()
    yes = subprocess.Popen(["yes"], stdout=subprocess.PIPE)
    subprocess.run(["openai", "tools", "fine_tunes.prepare_data", "-f", "data.jsonl"], stdin=yes.stdout)