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
    temperature = f'Температура за бортом {main.find(class_='p-forecast__temperature-value').text}'
    felt_temperature = f'ощущается как {main.find(class_='p-forecast__data').text}'
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


def detailed_weather_forecast_for_today():
    url = 'https://pogoda.mail.ru/prognoz/novosibirsk/14dney/#day2'
    html = bs(get(url, timeout=5).content, 'html.parser')
    main = html.find(class_='block block_collapse_top')

    data = main.find(class_='hdr__wrapper').text

    # Находим все блоки с классом 'p-flex__column p-flex__column_percent-16'
    period_blocks = main.find_all(class_='p-flex__column p-flex__column_percent-16')

    # Определяем периоды
    periods = ['night', 'morning', 'day', 'evening']
    results = {}

    for i, period in enumerate(periods):
        period_block = period_blocks[i]
        temperature = period_block.find(class_='text text_block text_bold_medium margin_bottom_10').text
        felt_temperature = period_block.find(class_='text text_block text_light_normal text_fixed color_gray').text
        description = period_block.find(class_='text text_block text_light_normal text_fixed').text

        # Определяем иконку в зависимости от описания
        if 'облачность' in description or 'облачно' in description:
            icon = '⛅️'
        elif 'ясно' in description or 'солнечно' in description:
            icon = '☀️'
        elif 'гроза' in description:
            icon = '⛈'
        else:
            icon = '🌧'

        results[period] = {
            'temperature': temperature,
            'felt_temperature': felt_temperature,
            'description': description,
            'icon': icon
        }

    return (data,
            results['night']['temperature'], results['night']['felt_temperature'], results['night']['description'],
            results['night']['icon'],
            results['morning']['temperature'], results['morning']['felt_temperature'],
            results['morning']['description'], results['morning']['icon'],
            results['day']['temperature'], results['day']['felt_temperature'], results['day']['description'],
            results['day']['icon'],
            results['evening']['temperature'], results['evening']['felt_temperature'],
            results['evening']['description'], results['evening']['icon'],
            )
