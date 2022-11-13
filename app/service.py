import requests
from config.settings import TELEGRAM_TOKEN, CHAT_ID, APP_ID
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination


chat_id = CHAT_ID
telegram_token = TELEGRAM_TOKEN
app_id = APP_ID


def Weather(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=' + app_id
        res = requests.get(url).json()
        city_info = {
            'city' : city,
            'temp' : res['main']['temp'],
            'icon' : res['weather'][0]['icon'],
            }
    except:
        city_info = None
        
    return city_info

def TelegrammMessage(message):
    requests.get('https://api.telegram.org/bot{}/sendMessage'.format(telegram_token), params=dict(
    chat_id=chat_id,
    text=message))


def get_client_ip(request):
    x_forwardet_for = request.META.get('X_FORWARDED_FOR')
    if x_forwardet_for:
        ip = x_forwardet_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip 


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id or request.user.is_staff


class PostPage(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CustomPage(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000