import time
from datetime import datetime
import pyautogui
import pywhatkit as kit
import pyperclip
import querier

def monitor_message():
    placeholder = ""
    while True:
        time.sleep(5)
        x1, y1 = [300,-600]
        x2, y2 = [1776,-144] # Apenas durante os testes
        #x2, y2 = [745,-144]
        x3, y3 = [1635,-434] # Apenas durante os testes
        #x3, y3 = [831,-434]

        pyautogui.moveTo(x1,y1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(x2,y2)
        pyautogui.rightClick()
        time.sleep(1)
        pyautogui.moveTo(x3,y3)
        pyautogui.click()
        time.sleep(1)
        text = pyperclip.paste()

        if "[QUERY]" in text and placeholder != text:
            placeholder = text
            process_message(text)
        print(". \n")
    

def process_message(text):
    instruction = "Traduza a mensagem a seguir para espanhol, responsa apenas com a tradução: "
    message = instruction + text
    result = querier.send_message(message)
    reply_message("+5521982736561",result)

def reply_message(phone_number, message):
    #hour = datetime.now().hour
    #minute = datetime.now().minute + 2
    #kit.sendwhatmsg(phone_number, message, time_hour=hour, time_min=minute)

    x4, y4 = [800,-80]
    pyautogui.moveTo(x4,y4)
    pyautogui.click()
    pyautogui.typewrite(message)
    pyautogui.press("enter")

monitor_message()






