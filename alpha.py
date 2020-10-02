# Virtual assistant Alpha
# Coded by A. Petek

import PySimpleGUI as sg
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha
import json
import requests
import random
import pyaudio
import webbrowser
import json
import warnings
from json import (load as jsonload, dump as jsondump)
from os import path
from ecapture import ecapture as ec


warnings.filterwarnings('ignore')
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.1)
        audio=r.listen(source)
        try:
            statement=r.recognize_google(audio,language='en-US')
            print(f"User said: {statement}\n")
        except Exception as e:
            return "None"
        return statement

def wakeWord(text):
    WAKE_WORDS = ['alpha'] 
    text = text.lower()
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    return False



SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'theme': sg.theme()}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'theme': '-THEME-'}

def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings


def save_settings(settings_file, settings, values):
    if values:      
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Settings saved')

def create_settings_window(settings):
    sg.theme(settings['theme'])

    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))

    layout = [  [sg.Text('Settings', font='Any 15')],
                [TextLabel('Theme'),sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
                [sg.Button('Save'), sg.Button('Exit')]  ]

    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)

    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')

    return window

def create_main_window(settings):
    sg.theme(settings['theme'])
    menu_def = [['&Menu', ['&Settings', 'E&xit']],
                ['&Help', '&About...']]

    right_click_menu = ['Unused', ['Settings', 'E&xit']]

    layout = [[sg.Menu(menu_def)],
          [sg.Text('Welcome! I am your Virtual Assistant Alpha.', font=('Comic sans ms', 10), size=(59,1)), sg.Text('Projects Support', font=('Helvetica', 9))],
          [sg.Text('', size=(60,1)), sg.Button('', key='paypal', size=(12,1), font=('Helvetica', 9), button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                               image_filename='paypal.png', image_size=(80, 50), image_subsample=2, border_width=0)],
          [sg.Text('Please speak.(Wake word Alpha)', font=('Comic sans ms', 8))],
          [sg.Output(size=(80, 17), key='out')]]

    return sg.Window('Alpha',
                     location=(738, 268),
                     right_click_menu=right_click_menu).Layout(layout)






def main():
    window, settings = None, load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )
    while True:
        if window is None:
            window = create_main_window(settings)
        button, value = window.Read(timeout=0.1)
        statement = takeCommand().lower()
        if (wakeWord(statement) == True):
            print("I am ready")
            speak("I am ready")
            statement = takeCommand().lower()
            if statement==0:
                continue

            elif "hello" in statement or "hi" in statement or "hey" in statement:
                    hour=datetime.datetime.now().hour
                    if hour>=0 and hour<12:
                        print("Hello,Good Morning")
                        speak("Hello,Good Morning")
                    elif hour>=12 and hour<18:
                        print("Hello,Good Afternoon")
                        speak("Hello,Good Afternoon")
                    else:
                        print("Hello,Good Evening")
                        speak("Hello,Good Evening")

            elif "goodbye" in statement or "ok bye" in statement or "stop" in statement:
                print('Your virtual assistant Alpha is shutting down,Good bye')
                speak('your virtual assistant Alpha is shutting down,Good bye')
                break

            elif 'wikipedia' in statement:
                try:
                    speak('Searching Wikipedia...')
                    statement =statement.replace("wikipedia", "")
                    results = wikipedia.summary(statement, sentences=3)
                    print("According to Wikipedia")
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError as e:
                    s = random.choice(e.options)
                    print(s)
                    speak(s)
                except wikipedia.exceptions.WikipediaException as e:
                    print('Search not include, try again wikipedia and your search')
                else:
                    continue
  
                

            elif 'open youtube' in statement:
                webbrowser.open_new_tab("https://www.youtube.com")
                print("Youtube is open now")
                speak("youtube is open now")
                

            elif 'open google' in statement:
                webbrowser.open_new_tab("https://www.google.com")
                print("Google chrome is open now")
                speak("Google chrome is open now")
                

            elif 'open gmail' in statement:
                webbrowser.open_new_tab("https://bit.ly/3iOcR5z")
                print("Google Mail open now")
                speak("Google Mail open now")
                

            elif "weather" in statement:
                api_key="394d4ebf0a7de20604147666d665d2d0"
                base_url="https://api.openweathermap.org/data/2.5/weather?"
                print("Whats the city name")
                speak("whats the city name")
                city_name=takeCommand()
                complete_url=base_url+"appid="+api_key+"&q="+city_name
                response = requests.get(complete_url)
                x=response.json()
                if x["cod"]!="404":
                    y=x["main"]
                    current_temperature = y["temp"]
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    print(city_name+" Temperature in kelvin unit = "+
                          str(current_temperature) +
                          "\n humidity (in percentage) = " +
                          str(current_humidiy) +
                          "\n description = " +
                          str(weather_description))
                    speak(city_name+" Temperature in kelvin unit is"+
                          str(current_temperature) +
                          "\n humidity in percentage is " +
                          str(current_humidiy) +
                          "\n description  " +
                          str(weather_description))
                else:
                    print(" City Not Found\n")
                    speak(" City Not Found ")
                    

            elif 'time' in statement:
                strTime=datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                print(f"The time and date is {strTime}")
                speak(f"the time and date is {strTime}")

            elif 'who are you' in statement or 'what can you do' in statement:
                print('I am Aplha version 1 point O your virtual assistant. I am programmed to do minor tasks like'
                      'opening youtube,google chrome,gmail and facebook ,predict time,take a photo,search wikipedia, predict weather' 
                      'in different cities , get top headline news from CNN and you can ask me computational or geographical questions too!')
                speak('I am Alpha version 1 point O your virtual assistant. I am programmed to do minor tasks like'
                      'opening youtube,google chrome,gmail and facebook ,predict time,take a photo,search wikipedia, predict weather' 
                      'in different cities , get top headline news from CNN and you can ask me computational or geographical questions too!')



            elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
                print("I was built by Adrijan")
                speak("I was built by Adrijan")
                

            elif "open facebook" in statement:
                webbrowser.open_new_tab("https://sl-si.facebook.com/")
                print("Facebook is open now")
                speak("Facebook is open now")
            

            elif 'news' in statement:
                news = webbrowser.open_new_tab("https://edition.cnn.com/")
                print('Here are some headlines from the CNN,Happy reading')
                speak('Here are some headlines from the CNN,Happy reading')
                

            elif "camera" in statement or "take a photo" in statement:
                ec.capture(0,"robo camera","img.jpg")
                print('Here is your photo')
                speak('Here is your photo')

            elif 'search'  in statement:
                statement = statement.replace("search", "")
                webbrowser.open_new_tab(statement)
                print('Here is your search')
                speak('Here is your search')
                

            elif 'ask' in statement:
                print('I can answer to computational and geographical questions and what question do you want to ask now')
                speak('I can answer to computational and geographical questions and what question do you want to ask now')
                question=takeCommand()
                app_id="47RWRU-LR6849249K"
                client = wolframalpha.Client('47RWRU-LR6849249K')
                res = client.query(question)
                answer = next(res.results).text
                print(answer)
                speak(answer)
                

            elif "joke" in statement:
                with open("joke.txt", "r") as m:
                    sents = m.read().split("\n\n")
                    se = random.choice(sents)
                    print(se)
                    speak(se)
                    

            elif "commands" in statement:
                print("commands are:"+"\n"+
                      "alpha"+
                      "hello, hi or hey"+
                      "good bye, ok bye or stop"+"\n"+
                      "wikipedia 'your search'"+"\n"+
                      "open youtube"+"\n"+
                      "open google"+"\n"+
                      "open gmail"+"\n"+
                      "weather 'city name'"+"\n"+
                      "time"+"\n"+
                      "who are you or what can you do"+"\n"+
                      "who made you or who created you"+"\n"+
                      "open facebook"+"\n"+
                      "news"+"\n"+
                      "camera or take a photo"+"\n"+
                      "search 'your choice'"+"\n"+
                      "ask 'your choice'"+"\n"+
                      "log off or sing out"+"\n"+
                      "joke")
                speak("commands are:"+
                      "alpha"+
                      "hello, hi or hey"+
                      "good bye, ok bye or stop"+
                      "wikipedia 'your search'"+
                      "open youtube"+
                      "open google"+
                      "open gmail"+
                      "weather 'city name'"+
                      "time"+
                      "who are you or what can you do"+
                      "who made you or who created you"+
                      "open facebook"+
                      "news"+
                      "camera or take a photo"+
                      "search 'your choice'"+
                      "ask 'your choice'"+
                      "log off or sing out"+
                      "joke")
                    

            elif "log off" in statement or "sign out" in statement:
                print("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                subprocess.call(["shutdown", "/l"])


        elif button == 'Settings':
            event, values = create_settings_window(settings).read(close=True)
            if event == 'Save':
                window.close()
                window = None
                save_settings(SETTINGS_FILE, settings, values)

        elif button == 'About...':
            sg.popup('About:', 'Created by Adrijan P.', 'Virtual Assistant:'+'\n\n'+'Alpha', 'Version 1.0')

        elif button == 'paypal':
            webbrowser.open_new_tab("https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=PFB6A6HLAQHC2&source=url")

        elif button in (None, 'Exit'):
            break

    window.close()

        
main()
