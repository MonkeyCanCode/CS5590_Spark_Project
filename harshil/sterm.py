#!/bin/python3

import sys
import json
import tweepy

CONSUMER_KEY = 'ZLxqFQ6xSU126W3gWt2Azz9jl'
CONSUMER_SECRET = 'Zn5dgjA1Np1APe5hEy7EHtJ74AN4BzPFeE827J4D8iI4soUT4b'
ACCESS_TOKEN = '976045398-tU7WUKUzYRjJZgDHfVCe8g30BWFrh7YPJubQ9BXa'
ACCESS_TOKEN_SECRET = 'wLRUBC8Q0kUrfK4CL069MHsu6PhQPu3iYcL3oVk88tjHH'

def validTweet(str_tweet):
    json_tweet = json.loads(str_tweet)
    return False if list(json_tweet.keys())[0] == 'delete' or list(json_tweet.keys())[0] == 'limit' else True

class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self, max_tweet=1):
        super(TwitterStreamListener, self).__init__()
        self.tweet_number = 0
        self.max_tweet = max_tweet

    def on_data(self, data):
        if self.tweet_number < self.max_tweet:
            if validTweet(data):
                with open('data.json', 'a') as f:
                    print(data, file=f)
                #print(data)
                print(self.tweet_number)
                self.tweet_number += 1
        else:
            sys.exit(0)

    def on_error(self, status):
        print(status)

def main():
    global CONSUMER_KEY
    global CONSUMER_SECRET
    global ACCESS_TOKEN
    global ACCESS_TOKEN_SECRET
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = tweepy.Stream(auth, TwitterStreamListener(100000))
    stream.filter(languages=['en'], track=['voting', 'senate','trump','house'])

if __name__ == '__main__':
    main()