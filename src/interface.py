import time
import os
import pyautogui
import pyperclip
import querier
import logging

logging.basicConfig(level=logging.INFO)

APP_LINK = r"C:\Users\Roberto\Desktop\WhatsApp.lnk"
CONTENT_PATH = "./data/downloaded"


def open_interface():
    logging.info(f"Abrindo WhatsApp desktop...")

    path = APP_LINK
    exit_code = os.system(path)
    if exit_code == 1:
        logging.error("Link do whatsapp não está disponível no caminho especificado.")
    time.sleep(5)
    monitor_message()


def monitor_message():
    logging.info(f"Monitorando mensagens...")
    reference_image = r"C:\Users\Roberto\OneDrive\Projetos\Assistente Contra Golpes\assets\copy-icon-2.png"
    placeholder = ""
    while True:
        time.sleep(5)
        x1, y1 = [235, 195]  # Último contato
        x2, y2 = [
            1605,
            953,
        ]  # Última mensagem (Apenas durante os testes / automensagem)
        # x2, y2 = [675,947] # Última mensagem
        x3, y3 = [
            1660,
            640,
        ]  # Opção de cópia, no menu de contexto (Apenas durante os testes / automensagem)
        # x3, y3 = [730,635] # Opção de cópia, no menu de contexto

        pyautogui.moveTo(x1, y1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(x2, y2)
        pyautogui.rightClick()
        time.sleep(1)
        # pyautogui.moveTo(x3,y3)
        img_coord = pyautogui.locateCenterOnScreen(reference_image)
        pyautogui.moveTo(img_coord)
        time.sleep(1)
        pyautogui.doubleClick()
        time.sleep(1)
        text = pyperclip.paste()

        if "[QUERY]" in text and placeholder != text:
            logging.info(f"Detectada mensagem com keyword.")
            placeholder = text
            process_message(text)
        print(".")


def read_files(folder_path):
    logging.info(f"Juntando todos os arquivos de grounding...")
    combined_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                combined_text += file.read() + "\n"
    return combined_text


def process_message(text):
    grounding = read_files(CONTENT_PATH)
    instruction = (
        "Com base nos textos de recomendação a seguir, responda a dúvida ao final."
    )
    message = instruction + grounding + text
    logging.info(f"Enviando payload ao GPT...")
    result = querier.send_message(message)
    reply_message(result)


def reply_message(message):
    logging.info(f"Transmitindo resposta...")
    x4, y4 = [540, 1015]  # Caixa de entrada de texto
    pyautogui.moveTo(x4, y4)
    pyautogui.click()
    time.sleep(1)
    pyautogui.typewrite(message, interval=0.1)
    time.sleep(1)
    pyautogui.press("enter")
    logging.info(f"Sucesso.")


if __name__ == "__main__":
    open_interface()
