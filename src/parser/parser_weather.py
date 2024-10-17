from random import choice

import datetime

from bs4 import BeautifulSoup as bs
from requests import get


def hourly_weather_forecast():
    """ Returns the hourly forecast for the given weather station """
    now = datetime.datetime.now()
    hours = now.hour

    name = choice(
        ['Солнышко', 'Булочка', 'Лапочка']
    )

    if 5 < hours < 11:
        answer = choice(
            [f'Доброе утро {name}!', f'Просыпайся моя {name}!', 'С добрый утром мой солёненький кренделёчек!']
        )
    elif 11 < hours < 17:
        answer = choice(
            [f'Добрый день {name}!', f'Прекрасного дня {name}!']
        )
    elif 17 < hours < 23:
        answer = choice(
            [f'Приятного вечера {name}!', f'Спокойного вечера {name}!']
        )
    elif 23 < hours < 24 or 0 < hours < 5:
        answer = choice(
            [f'Доброй ночи {name}!', f'Сладниъ снов {name}!', f'Расслабляйся {name}']
        )
    else:
        answer = f'{name}'

    url = 'https://pogoda.mail.ru/prognoz/novosibirsk/24hours/'
    html = bs(get(url, timeout=5).content, 'html.parser')
    main = html.find(class_='p-forecast__header-inner')

    data = main.find(class_='p-forecast__title').text
    temperature = f'Температура за бортом {main.find(class_='p-forecast__temperature-value').text}, '
    felt_temperature = f'ощущается как {main.find(class_='p-forecast__data').text}.'
    description = f'На улице {main.find(class_='p-forecast__description').text}'

    if 'облачность' in description or 'облачно' in description:
        icon = '⛅️'
    elif 'ясно' in description or 'солнечно' in description:
        icon = '☀️'
    elif 'гроза' in description:
        icon = '⛈'
    else:
        icon = '🌧'

    return data, answer, temperature, felt_temperature, description, icon
