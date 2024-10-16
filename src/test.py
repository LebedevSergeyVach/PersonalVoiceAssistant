#
# r.adjust_for_ambient_noise(sourse, duration=3)
#
#
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))


import pyttsx3
import speech_recognition
import speech_recognition as sr
import pyaudio
import webbrowser


r = sr.Recognizer()
voice = pyttsx3.init()
voice.say("Привет!")
voice.runAndWait()

while True:
    with sr.Microphone(device_index=1) as source:
        try:
            print("Скажите что-нибудь...")
            audio = r.listen(source)
            speech = r.recognize_google(audio, language="ru-RU").lower()
        except speech_recognition.UnknownValueError:
            voice.say("Я вас не понимаю...")
            voice.runAndWait()
        else:
            print(speech)
            if speech.find("привет") >= 0:
                voice.say("Привет!")
                voice.runAndWait()
            elif speech.find("ютуб") >= 0 or speech.find("youtube") >= 0:
                webbrowser.open_new("https://www.youtube.com")
                voice.say("Ютуб запущен")
                voice.runAndWait()
            else:
                voice.say("Я вас не понимаю ...")
                voice.runAndWait()
