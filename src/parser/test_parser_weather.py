from parser_weather import hourly_weather_forecast, detailed_weather_forecast_for_today

# print('Проверка прогноза погоды сейчас, функция hourly_weather_forecast()')
# print(hourly_weather_forecast())
#
# print('\nПроверка подробного прогноза погоды, функция detailed_weather_forecast_for_today()')
# print(detailed_weather_forecast_for_today())

print('Test message')
data, answer, temperature, felt_temperature, description, icon = hourly_weather_forecast()
weather = f'{answer}\n{temperature}, {felt_temperature}.\n{description} {icon}'

print(f'Message: {weather}')

print('\nTest message')
(data,
 night_temperature, night_felt_temperature, night_description, night_icon,
 morning_temperature, morning_felt_temperature, morning_description, morning_icon,
 day_temperature, day_felt_temperature, day_description, day_icon,
 evening_temperature, evening_felt_temperature, evening_description, evening_icon,
 ) = detailed_weather_forecast_for_today()

weather_message = (f'{data}\n'
                   f'Ночью: {night_temperature}, {night_felt_temperature}, {night_description} {night_icon}\n'
                   f'Утром: {morning_temperature}, {morning_felt_temperature}, '
                   f'{morning_description} {morning_icon}\n'
                   f'Днем: {day_temperature}, {day_felt_temperature}, {day_description} {day_icon}\n'
                   f'Вечером: {evening_temperature}, {evening_felt_temperature}, '
                   f'{evening_description} {evening_icon}'
                   )

print(f'Message: {weather_message}')
