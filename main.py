import tweepy
import credentials
from time import sleep
from datetime import datetime, timezone
from pytz import timezone

est = timezone('US/Eastern')


consumer_key = credentials.env['consumer_key']
consumer_secret = credentials.env['consumer_secret']
access_token = credentials.env['access_token']
access_token_secret = credentials.env['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

while True:
    new_tweet = 'Timestamp: ' + str(datetime.now(est))
    api.update_status(status=new_tweet)
    sleep(900) # 15 minutes