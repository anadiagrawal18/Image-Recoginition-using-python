#Program to say what it inputs

import pyttsx3
import datetime

def speak(audio):
    """Speaks what it get in input"""
    a = pyttsx3.init('sapi5') 
    a.say(audio)
    a.runAndWait()

def telltime():
    """Tell's current time"""
    crt = datetime.datetime.now().strftime("%H:%M")
    print(f"It's {crt}\n")
    speak(f"It's {crt}")




def tdate():
    """Tell's current day and the date"""
    crd =datetime.datetime.now().date()
    crda =datetime.datetime.today().strftime('%A')
    
    print(f"Today's Day is {crda}")
    speak(f"Today's Day is {crda}")
    
    print(f"Today's Date is {crd}\n")
    speak(f"Today's Date is {crd}")