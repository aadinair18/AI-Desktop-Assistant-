from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QMovie
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit as wk
import os
import random
import cv2
import sys
import time
import pyautogui
import operator
import requests
import psutil
import openai
from testconfig import name,apikey
import subprocess
# from lsHotword.ls import Hotword


flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)

engine = pyttsx3.init('sapi5')  # this is microsoft's speech api
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)  # voices has 2 elements a male and female voice as 0 and 1 respectively
engine.setProperty('rate', 150)  # this sets the speed of the voice

from pygame import mixer
mixer.init()
beep = mixer.Sound("C:\\Users\\Vince\\Music\\ping-82822.mp3")

path_to_model = "C:\\Users\\Vince\\PycharmProjects\\MajorProjectsem7\\GUI-Jarvis-main\\model.h5"          # path to model where it is located
# wake = Hotword(path_to_model)
#
# hotwordflag = True
# loopflag = True

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am at your service, What can I do for you?")
    speak("If you would like to see the list of commands please say open help guide")

def ai(query):
    openai.api_key = apikey
    query += f" in 2 sentences"
    content = f"OpenAI response for the promt: {query}  \n ****************** \n\n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": query
            },
            {
                "role": "user",
                "content": ""
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: wrap this in try catch block
    answer = response["choices"][0]["message"]["content"]
    print(answer)
    speak(answer)


class mainT(QThread):
    def __init__(self):
        super(mainT,self).__init__()
    
    def run(self):
        self.JARVIS()

    def takecommand(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            beep.play()
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 0.5  # Pause threshold another accessibility fucntion
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            print("Say that again please...")
            speak("Say that again please...")
            return "None"
        return query

    def reactivate(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            #beep.play()
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1  # Pause threshold another accessibility fucntion
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception as e:
            # print("Say that again please...")
            # speak("Say that again please...")
            return "None"
        return query

    def JARVIS(self):
        wish()
        while True:
            query = self.takecommand().lower()
            if "what is the time" in query:
                hour = datetime.datetime.now().strftime("%H")
                hour = str(int(hour) % 12)
                min = datetime.datetime.now().strftime("%M")
                speak(f"The time is {hour}:{min}")

            elif "open help guide" in query:
                npath = "D:\College\Major project sem 7\GUI-Jarvis-main\helpguide.txt"
                os.startfile(npath)

            elif "what is my ip address" in query:
                speak("checking")
                try:
                    address = requests.get('https://api.ipify.org').text
                    print(address)
                    speak("your ip address is ")
                    speak(address)

                except Exception as e:
                    speak("Unable to reach server due to network issues, please try later")

            elif "what is" in query:
                speak("Searching Wikipedia...")
                try:
                    query = query.replace("what is", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except Exception as e:
                    speak("I didnt quite catch that please ask again")

            elif "who is" in query:  # For wikipedia
                speak("Searching Wikipedia...")
                try:
                    query = query.replace("who is", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except Exception as e:
                    speak("I didnt quite catch that please ask again")

            elif "just open google" in query:  # for google
                webbrowser.open('http://google.com')

            elif "open google" in query:
                speak("what do you want to search?")
                request = self.takecommand().lower()
                webbrowser.open(
                    f"https://duckduckgo.com/?q={request}")  # https://duckduckgo.com/?q=is+my+query&t=brave&ia=web
                try:
                    results = wikipedia.summary(request, sentences=1)
                    speak(results)
                except Exception as e:
                    continue

            elif "just open youtube" in query:  # for youtube
                webbrowser.open('https://www.youtube.com')

            elif "open youtube" in query:
                speak("what do you want to watch?")
                request = self.takecommand().lower()
                wk.playonyt(f"{request}")

            elif "search on youtube" in query:
                query = query.replace("search on youtube", "")
                webbrowser.open(f"www.youtube.com/results?search_query={query}")

            elif "using artificial intelligence" in query:
                ai(query)

            elif "open browser" in query:  # for closing browser
                npath = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
                os.startfile(npath)

            elif "close browser" in query:  # for closing browser
                os.system("taskkill /f /im brave.exe")

            elif "open paint" in query:
                npath = "C:\WINDOWS\system32\mspaint.exe"
                os.startfile(npath)

            elif "close paint" in query:
                os.system("taskkill /f /im mspaint.exe")

            elif "open notepad" in query:
                npath = "C:\WINDOWS\system32\\notepad.exe"
                os.startfile(npath)

            elif "make a note" in query:
                npath = "C:\WINDOWS\system32\\notepad.exe"
                os.startfile(npath)
                # speak("what should i name the note")
                # name = takecommand().lower()
                speak("tell me what to write")
                note = self.takecommand().lower()
                pyautogui.typewrite(note, 0.07)

                speak("please name the file")
                name = self.takecommand().lower()
                time.sleep(1)
                pyautogui.hotkey('ctrl', 's')
                time.sleep(1)
                pyautogui.typewrite(name)
                time.sleep(0.5)
                pyautogui.press('enter')
                speak("done")
                speak("closing notepad")
                os.system("taskkill /f /im notepad.exe")




            elif "close notepad" in query:
                os.system("taskkill /f /im notepad.exe")

            elif "open command prompt" in query:
                os.system("start cmd")

            elif "close command prompt" in query:
                os.system("taskkill /f /im cmd.exe")

            elif "play music" in query:
                music_dir = "C:\\Users\\Vince\\Music"
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, random.choice(songs)))

            elif "stop music" in query:
                os.system("taskkill /f /im vlc.exe")

            elif "shut down the system" in query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in query:
                os.system("shutdown /r /t 5")

            elif "deactivate" in query:
                speak("Deactivating, to wake me up please say activate")
                flag_activate = True
                while flag_activate:
                    word = self.reactivate().lower()
                    if 'activate' in word:
                        flag_activate = False
                wish()

            # elif "lock the system" in query:
            #     os.system(r'rundll32.exe powrprof.dll,SetSuspendState Hibernate')

            elif "check battery" in query:
                battery_detecting = psutil.sensors_battery()
                plugged = battery_detecting.power_plugged
                percent_battery = str(battery_detecting.percent)
                plugged = "Plugged In" if plugged else "Not Plugged In"
                print(percent_battery + '% | ' + plugged)
                speak(percent_battery + '% | ' + plugged)

            elif "open camera" in query:
                subprocess.run('start microsoft.windows.camera:', shell=True)

            elif "take a photo" in query:
                subprocess.run('start microsoft.windows.camera:', shell=True)
                time.sleep(1)
                speak("get ready for the photo in 5 seconds")
                time.sleep(5)
                pyautogui.press('enter')
                time.sleep(1)
                speak('Closing camera')
                subprocess.run('Taskkill /IM WindowsCamera.exe /F', shell=True)

            elif "go to sleep" in query:
                speak("Ok, going to sleep")
                sys.exit()

            elif "take screenshot" in query:
                speak("What should I name the screenshot")
                name = self.takecommand().lower()
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"C:\\Users\\Vince\\Pictures\\Screenshots\\{name}.png")
                speak("Screenshot saved")

            elif "calculate" in query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("ready")
                    print("Listening...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)

                def get_operator_fn(op):
                    return {
                        '+': operator.add,
                        '-': operator.sub,
                        'into': operator.mul,
                        'divided by': operator.__truediv__,
                    }[op]

                def eval_binary_expr(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)

                speak("your result is")
                speak(eval_binary_expr(*(my_string.split())))


            elif "volume up" in query:
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup")

            elif "volume down" in query:
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")

            elif "mute" in query:
                pyautogui.press("volumemute")

            elif "unmute" in query:
                pyautogui.press("volumeunmute")


            elif "please write" in query:
                query = query.replace("please write ", "")
                pyautogui.typewrite(query, 0.1)

            elif "maximize" in query:
                pyautogui.hotkey("win", "up")
                pyautogui.hotkey("win", "up")

            elif "minimise" in query:
                pyautogui.hotkey("win", "down")
                pyautogui.hotkey("win", "down")


            elif "save" in query:
                pyautogui.hotkey('ctrl', 's')

            elif "copy" in query:
                pyautogui.hotkey('ctrl', 'c')

            elif "paste" in query:
                pyautogui.hotkey('ctrl', 'v')

            elif "undo" in query:
                pyautogui.hotkey('ctrl', 'z')

            elif "redo" in query:
                pyautogui.hotkey('ctrl', 'y')

            elif "select all" in query:
                pyautogui.hotkey('ctrl', 'a')

            elif "task manager" in query:
                pyautogui.hotkey('ctrl', 'shift', 'esc')

            elif "change tab" in query:
                pyautogui.hotkey('alt', 'tab')

            elif "press right" in query:
                pyautogui.press('right')

            elif "press down" in query:
                pyautogui.press('down')

            elif "press up" in query:
                pyautogui.press('up')

            elif "press windows" in query:
                pyautogui.press('win')

            elif "close" in query:
                pyautogui.hotkey('alt', 'f4')

            elif "press enter" in query:
                pyautogui.press('enter')

            elif "press escape" in query:
                pyautogui.press('esc')

            elif "press space" in query:
                pyautogui.press('space')

            elif "scroll up" in query:
                pyautogui.scroll(500)

            elif "scroll down" in query:
                pyautogui.scroll(-500)

            elif "move mouse right" in query:
                pyautogui.moveRel(100,0,0.5)

            elif "move mouse left" in query:
                pyautogui.moveRel(-100,0,0.5)

            elif "move mouse up" in query:
                pyautogui.moveRel(0,-100,0.5)

            elif "move mouse down" in query:
                pyautogui.moveRel(0,100,0.5)

            elif "left click" in query:
                pyautogui.click()

            elif "right click" in query:
                pyautogui.click(button='right')

            elif "double click" in query:
                pyautogui.click(clicks=2, interval=0.25)


            elif "jarvis" in query:
                print("Hello How may I help you")
                speak("Hello How may I help you")

            elif "hi" in query:
                print("Hello How may I help you")
                speak("Hello How may I help you")

            elif "hello" in query:
                print("Hello How may I help you")
                speak("Hello How may I help you")

            elif "who are you" in query:
                print("My name is Jarvis and I am here to assist you")
                speak("My name is Jarvis and I am here to assist you")

            elif "what are you" in query:
                print("I am a Virtual Desktop assistant, created and designed to help you from your computer.")
                speak("I am a Virtual Desktop assistant, created and designed to help you from your computer.")

            elif "thank you" in query:
                print("You are welcome, I'm happy to help")
                speak("You are welcome, I'm happy to help")

FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"./scifi.ui"))

class Main(QMainWindow,FROM_MAIN):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(1920,1080)
        self.label_7 = QLabel
        self.exitB.setStyleSheet("background-image:url(./lib/exit - Copy.png);\n"
        "border:none;")
        self.exitB.clicked.connect(self.close)
        self.setWindowFlags(flags)
        Dspeak = mainT()
        self.label_7 = QMovie("./lib/gifloader.gif", QByteArray(), self)
        self.label_7.setCacheMode(QMovie.CacheAll)
        self.label_4.setMovie(self.label_7)
        self.label_7.start()

        self.ts = time.strftime("%A, %d %B")

        Dspeak.start()
        self.label.setPixmap(QPixmap("./lib/tuse.png"))
        self.label_5.setText("<font size=8 color='white'>"+self.ts+"</font>")
        self.label_5.setFont(QFont(QFont('Acens',8)))


app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
exit(app.exec_())