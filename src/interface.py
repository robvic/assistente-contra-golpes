import time
import os
import pyautogui
import pyperclip
import querier

# TO-DO:
# - Workaround sobre janela de notificações.

def monitor_message():
    placeholder = ""
    while True:
        time.sleep(5)
        x1, y1 = [235,195] # Último contato
        x2, y2 = [1605,953] # Última mensagem (Apenas durante os testes / automensagem)
        #x2, y2 = [675,947] # Última mensagem
        x3, y3 = [1660,640] # Opção de cópia, no menu de contexto (Apenas durante os testes / automensagem)
        #x3, y3 = [730,635] # Opção de cópia, no menu de contexto

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
    instruction = "Traduza a mensagem a seguir para espanhol, responda apenas com a tradução: "
    message = instruction + text
    result = querier.send_message(message)
    reply_message(result)

def reply_message(message):
    x4, y4 = [800,-80] # Caixa de entrada de texto
    pyautogui.moveTo(x4,y4)
    pyautogui.click()
    pyautogui.typewrite(message)
    pyautogui.press("enter")

if __name__ == "__main__":
    path = r"C:\Users\Roberto\Desktop\WhatsApp.lnk"
    os.system(path)
    time.sleep(5)
    monitor_message()



