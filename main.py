import tweepy
import credentials
import logging
import pyowm
from time import sleep
from datetime import datetime, timezone
from pytz import timezone

emoji = {
    'partly_cloudy' : u'\U000026C5',
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

est = timezone('US/Eastern')

# Set credentials for Authentication
consumer_key = credentials.env['consumer_key']
consumer_secret = credentials.env['consumer_secret']
access_token = credentials.env['access_token']
access_token_secret = credentials.env['access_token_secret']
owm_key = credentials.env['owm_key']

# Tweepy setup
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# OpenWeatherMaps setup
owm = pyowm.OWM(owm_key)
observation = owm.weather_manager().weather_at_place('48150')
data = observation.weather
print(data.status)
print(data.temperature('fahrenheit'))

map = \
'.   ' + emoji['partly_cloudy'] + '\n' +\
'  ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '\n' +\
'   ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '\n' +\
\
\
'     ' + emoji['partly_cloudy'] + '\n' +\
'                    ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '\n' +\
'              ' + ' ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '\n' +\
'              ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '\n' +\
'             ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '  ' + emoji['partly_cloudy'] + '\n' +\
'             ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '\n' +\
'              ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '\n' +\
'              ' + ' ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '\n' +\
'              ' + ' ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '\n' +\
'              ' + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + emoji['partly_cloudy'] + '\n'\

print(map)

while True:
    #new_tweet = emoji['partly_cloudy'] + str(datetime.now(est))
    logger.info('Tweeting now...')
    api.update_status(status=map)
    sleep(900) # 15 minutes
