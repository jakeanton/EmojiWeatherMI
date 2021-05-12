import tweepy
import credentials
import logging
import pyowm
from time import sleep
from datetime import datetime, time
from pytz import timezone

zip_codes =  \
[
'49913',                                     \
'49968', '49946', '49855', '49839', '49783',         \
'49927', '49815', '49878', '49838', '49781', '49781',  \
'49887',                                     \
'49720', '49779',                              \
'49684', '49735', '49746', '49707',                   \
'49660', '49601', '48661', '48730',                   \
'49459', '49307', '48858', '48706', '48731',          \
'49445', '49343', '48847', '48655', '48461', '48401', \
'49417', '49503', '48860', '48867', '48503', '48060', \
'49423', '49325', '48910', '48350', '48048',          \
'49043', '49008', '49269', '48104', '48226',          \
'49128', '49091', '49242', '49221', '48162'           \
]

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

moon_emoji = {
    'new moon' : u'\U0001F311',
    'waxing crescent moon' : u'\U0001F312',
    'first quarter moon' : u'\U0001F313',
    'waxing gibbous moon' : u'\U0001F314',
    'full moon' : u'\U0001F315',
    'waning gibbous moon' : u'\U0001F316',
    'last quarter moon' : u'\U0001F317',
    'waning crescent moon' : u'\U0001F318',
}

def get_weather(zip_code):
    """ Returns the weather info for the supplied ZIP code """
    country = 'us'

    try:
        observation = owm.weather_manager().weather_at_zip_code(zip_code, country)
        data = observation.weather
        return data

    except:
        print(f'Error for {zip_code}')


def assign_emoji(data):
    """ Takes in weather data, returns the emoji representing the current weather conditions """
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
        elif ((data.detailed_status == 'scattered clouds') or
              (data.detailed_status == 'broken clouds')):
            return emoji['partly_cloudy']
        else: # full cloudcover == overcast clouds
            return emoji['full_cloudy']
    elif (data.status == 'Fog'):
        return emoji['fog']
    elif (data.status == 'Tornado'):
        return emoji['tornado']
    else: #Sand, Dust, Ash, Squall, Mist, Haze
        return emoji['fog']


def get_map(in_list):
    """ Takes in list of 55 emoji (mapped to each ZIP code), return Michigan """
    map = \
    '.   ' + in_list[0] + '\n' +\
    '  ' + in_list[1] + in_list[2] + in_list[3] + in_list[4] + in_list[5] + '\n' +\
    '   ' + in_list[6] + in_list[7] + in_list[8] + in_list[9] + in_list[10] + in_list[11] + '\n' +\
    \
    \
    '     ' + in_list[12] + '\n' +\
    '                    ' + in_list[13] + in_list[14] + '\n' +\
    '              ' + ' ' + in_list[15] + in_list[16] + in_list[17] + in_list[18] + '\n' +\
    '              ' + in_list[19] + in_list[20] + in_list[21] + in_list[22] + '\n' +\
    '             ' + in_list[23] + in_list[24] + in_list[25] + in_list[26] + '  ' + in_list[27] + '\n' +\
    '             ' + in_list[28] + in_list[29] + in_list[30] + in_list[31] + in_list[32] + in_list[33] + '\n' +\
    '              ' + in_list[34] + in_list[35] + in_list[36] + in_list[37] + in_list[38] + in_list[39] + '\n' +\
    '              ' + ' ' + in_list[40] + in_list[41] + in_list[42] + in_list[43] + in_list[44] + '\n' +\
    '              ' + ' ' + in_list[45] + in_list[46] + in_list[47] + in_list[48] + in_list[49] + '\n' +\
    '              ' + in_list[50] + in_list[51] + in_list[52] + in_list[53] + in_list[54] + '\n'
    return map


def is_it_daytime(data):
    """ Takes in weather data, returns True if it is daytime and False otherwise """
    est = timezone('US/Eastern')
    current_time = datetime.now(tz=est).time()
    sunrise = data.sunrise_time(timeformat='date').astimezone(tz=est).time()
    sunset = data.sunset_time(timeformat='date').astimezone(tz=est).time()

    return is_time_between(sunrise, sunset, current_time)


def is_time_between(begin_time, end_time, check_time):
    return check_time >= begin_time and check_time <= end_time


def is_time_to_tweet():
    est = timezone('US/Eastern')
    current_time = datetime.now(tz=est).time()

    if is_time_between(time(8,00),time(8,5), current_time) or \
       is_time_between(time(12,00),time(12,5), current_time) or \
       is_time_between(time(16,00),time(16,5), current_time) or \
       is_time_between(time(20,00),time(20,5), current_time):
        return True
    else:
        return False


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

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


    while True:
        logger.info('Tweeting now...')
        if is_time_to_tweet():

            emoji_list = []
            for zip_code in zip_codes:
                emoji_list.append(assign_emoji(get_weather(zip_code)))

            map = get_map(emoji_list)

            api.update_status(status=map)
            sleep(12600) # 3.5 hours
        else:
            sleep(60) # 1 minutes