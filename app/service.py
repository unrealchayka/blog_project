import requests
from config.settings import TELEGRAM_TOKEN, CHAT_ID, APP_ID

chat_id = CHAT_ID
telegram_token = TELEGRAM_TOKEN
app_id = APP_ID


def Weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=' + app_id
    res = requests.get(url).json()
    city_info = {
        'city' : city,
        'temp' : res['main']['temp'],
        'icon' : res['weather'][0]['icon'],
    }
    return city_info

def TelegrammMessage(message):
    requests.get('https://api.telegram.org/bot{}/sendMessage'.format(telegram_token), params=dict(
    chat_id=chat_id,
    text=message))