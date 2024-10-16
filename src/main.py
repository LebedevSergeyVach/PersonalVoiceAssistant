import speech_recognition as sr
import pyttsx3
import spacy
import threading
import queue
import sys

from parser.parser_weather import hourly_weather_forecast, detailed_weather_forecast_for_today
from meta.meta import MetaClass

# Инициализация распознавателя речи
recognizer = sr.Recognizer()

# Инициализация синтезатора речи
engine = pyttsx3.init()

# Загрузка русской модели spaCy
nlp = spacy.load('ru_core_news_sm')

# Очередь для хранения команд
command_queue = queue.Queue()

# Флаг для остановки потоков
stop_threads = False


# Функция для синтеза речи
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Функция для распознавания речи через микрофон
def recognize_speech_from_mic():
    global stop_threads
    while not stop_threads:
        try:
            with sr.Microphone() as source:
                print('Слушаю...')
                audio = recognizer.listen(source)
                try:
                    text = recognizer.recognize_google(audio, language='ru-RU')
                    print(f'Вы сказали: {text}')
                    command_queue.put(text)
                except sr.UnknownValueError:
                    print('Извините, я вас не понял')
                except sr.RequestError:
                    print('Извините, произошла ошибка при запросе к сервису распознавания речи')
        except Exception as e:
            print(f'Ошибка при работе с микрофоном: {e}')


# Функция для получения команды через терминал
def get_command_from_terminal():
    global stop_threads
    while not stop_threads:
        command = input()
        command_queue.put(command)


# Основной цикл
def main():
    global stop_threads

    # Вывод доступных голосов
    voices = engine.getProperty('voices')

    if MetaClass.showing_the_voice_selection:
        print('Доступные голоса:')
        for index, voice in enumerate(voices):
            print(f'{index}: {voice.name}, {voice.languages}, {voice.gender}, {voice.age}')

    # Выбор голоса
    voice_index = MetaClass.voice_index
    voice_speed = MetaClass.voice_speed
    voice_volume = MetaClass.voice_volume

    engine.setProperty('voice', voices[voice_index].id)

    # Настройка скорости речи и громкости
    engine.setProperty('rate', voice_speed)  # Скорость речи (слова в минуту)
    engine.setProperty('volume', voice_volume)  # Громкость (от 0.0 до 1.0)

    print('Помощник: Привет! Чем я могу вам помочь?')
    speak('Привет! Чем я могу вам помочь?')

    # Запуск потоков
    mic_thread = threading.Thread(target=recognize_speech_from_mic)
    terminal_thread = threading.Thread(target=get_command_from_terminal)
    mic_thread.start()
    terminal_thread.start()

    while True:
        if not command_queue.empty():
            text = command_queue.get()
            print(f'Вы: {text}')

            # Обработка текста с помощью spaCy
            doc = nlp(text.lower())
            if 'привет' in [token.text for token in doc]:
                print('Помощник: Привет! Как дела?')
                speak('Привет! Как дела?')
            elif 'пока' in [token.text for token in doc] or 'закрыть' in [token.text for token in doc]:
                print('Помощник: До свидания!')
                speak('До свидания!')
                stop_threads = True

                break
            elif ('погода' in [token.text for token in doc] or 'погод' in [token.text for token in doc]
                  or 'погоде' in [token.text for token in doc] or 'погоду' in [token.text for token in doc]):

                data, answer, temperature, felt_temperature, description, icon = hourly_weather_forecast()
                weather_message = (f'{answer}\n'
                                   f'{temperature}, {felt_temperature}.\n'
                                   f'{description} {icon}')

                speak(weather_message)
                print(f'Помощник: {weather_message}')
            elif ('время' in [token.text for token in doc] or 'времени' in [token.text for token in doc]
                  or 'дата' in [token.text for token in doc]):

                data, answer, temperature, felt_temperature, description, icon = hourly_weather_forecast()
                data_message = f'{data}'

                print(f'Помощник: {data_message}')
                speak(data_message)
            elif 'прогноз' in [token.text for token in doc]:

                (data,
                 night_temperature, night_felt_temperature, night_description, night_icon,
                 morning_temperature, morning_felt_temperature, morning_description, morning_icon,
                 day_temperature, day_felt_temperature, day_description, day_icon,
                 evening_temperature, evening_felt_temperature, evening_description, evening_icon,
                 ) = detailed_weather_forecast_for_today()

                weather_message = (f'{data}\n'
                                   f'Ночью: {night_temperature}, {night_felt_temperature}, '
                                   f'{night_description} {night_icon}\n'
                                   f'Утром: {morning_temperature}, {morning_felt_temperature}, '
                                   f'{morning_description} {morning_icon}\n'
                                   f'Днем: {day_temperature}, {day_felt_temperature}, '
                                   f'{day_description} {day_icon}\n'
                                   f'Вечером: {evening_temperature}, {evening_felt_temperature}, '
                                   f'{evening_description} {evening_icon}'
                                   )

                print(f'Помощник: {weather_message}')
                speak(weather_message)
            else:
                print('Помощник: Извините, я не понимаю вас.')
                speak('Извините, я не понимаю вас.')

    # Ожидание завершения потоков
    mic_thread.join()
    terminal_thread.join()

    # Завершение программы
    sys.exit(0)


if __name__ == '__main__':
    main()
