import tweepy
import credentials
import logging
import pyowm
from time import sleep
from datetime import datetime, timezone
from pytz import timezone

emoji = {
    'partly_cloudy' : u'\U000026C5',
    'mostly_sunny' : u'\U0001F324',
    'full_cloudy' : u'\U00002601',
    'thunderstorm' : u'\U0001F329',
    'tornado' : u'\U0001F32A',
    'rain' : u'\U0001F327',
    'snow' : u'\U00002744',
    'sunny' : u'\U00002600',
    'fog' : u'\U0001F32B',
}

def get_weather(zip):
    observation = owm.weather_manager().weather_at_place(zip)
    data = observation.weather
    return data

def assign_emoji(data):
    if (data.status == 'Thunderstorm'):
        return emoji['thunderstorm']
    elif (data.status == 'Drizzle' or data.status == 'Rain'):
        return emoji['rain']
    elif (data.status == 'Snow'):
        return emoji['snow']
    elif (data.status == 'Clear'):
        return emoji['sunny']
    elif (data.status == 'Clouds'):
        if (data.detailed_status == 'few clouds'):
            return emoji['mostly_sunny']
        elif (data.detailed_status == 'scattered clouds'):
            return emoji['partly_cloudy']
        else: #full cloudcover == broken clouds or overcast clouds
            return emoji['full_cloudy']
    elif (data.status == 'Fog'):
        return emoji['fog']
    elif (data.status == 'Tornado'):
        return emoji['tornado']
    else: #Sand, Dust, Ash, Squall, Mist, Haze
        return emoji['fog']
    
def get_emoji(zip):
    return assign_emoji(get_weather(zip))

if __name__ == '__main__':

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

    map = \
    '.   ' + emoji['sunny'] + '\n' +\
    '  ' + emoji['sunny'] + emoji['sunny'] + emoji['sunny'] + emoji['sunny'] + emoji['sunny'] + '\n' +\
    '   ' + emoji['sunny'] + emoji['sunny'] + emoji['sunny'] + emoji['sunny'] + emoji['sunny'] + emoji['sunny'] + '\n' +\
    \
    \
    '     ' + emoji['snow'] + '\n' +\
    '                    ' + emoji['snow'] + emoji['snow'] + '\n' +\
    '              ' + ' ' + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + '\n' +\
    '              ' + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + '\n' +\
    '             ' + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + '  ' + emoji['snow'] + '\n' +\
    '             ' + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + '\n' +\
    '              ' + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + '\n' +\
    '              ' + ' ' + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + '\n' +\
    '              ' + ' ' + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + '\n' +\
    '              ' + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + emoji['snow'] + '\n'\

    print(map)

    while True:
        logger.info('Tweeting now...')
        api.update_status(status=map)
        sleep(900) # 15 minutes
