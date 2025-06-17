import time
from datetime import datetime, timedelta
import os
import pyautogui
import pyperclip
import querier
import logging

# Logging configs
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_log = logging.StreamHandler()
console_log.setLevel(logging.INFO)
console_log.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

file_log = logging.FileHandler("./logs/log.txt")
file_log.setLevel(logging.DEBUG)
file_log.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

logger.addHandler(console_log)
logger.addHandler(file_log)

# Common vars
APP_LINK = os.path.join(
    os.path.join(os.environ["USERPROFILE"], "Desktop"), "WhatsApp.lnk"
)
CONTENT_PATH = "./data/downloaded"
IMAGES_PATH = "./assets"


def open_interface():
    logger.info(f"Abrindo WhatsApp desktop...")

    path = APP_LINK
    exit_code = os.system(path)
    if exit_code == 1:
        logger.error("Link do whatsapp não está disponível no caminho especificado.")
    time.sleep(5)
    monitor_message()


def monitor_message():
    logger.info(f"Monitorando mensagens...")
    placeholder = ""
    history = []
    time_check = datetime.now()
    while True:
        time.sleep(5)
        x1, y1 = [235, 195]  # Último contato
        #x2, y2 = [1605, 953]  # Última mensagem (Apenas durante os testes / automensagem)
        x2, y2 = [675, 947]  # Última mensagem

        pyautogui.moveTo(x1, y1)
        pyautogui.doubleClick()
        time.sleep(1)
        pyautogui.moveTo(x2, y2)
        pyautogui.rightClick()
        time.sleep(1)
        img_coord = find_image(IMAGES_PATH)
        if img_coord is  not None:
            pyautogui.moveTo(img_coord)
        else:
            logger.warning(f"Imagem não foi encontrada, pode estar na vez do reply ou a mensagem em questão é incompatível (links, imagens, etc).")
            continue
        time.sleep(1)
        pyautogui.doubleClick()
        time.sleep(1)
        text = pyperclip.paste()

        if placeholder != text:
            logger.info(f"Detectada mensagem nova.")
            placeholder = text
            if datetime.now() - time_check > timedelta(minutes=5):
                logger.info(f"Mensagem em nova sessão.")
                history = []
                time_check = datetime.now()
            else:
                logger.info(f"Mensagem em sessão já existente.")
                time_check = datetime.now()
            history = process_message(text, history)

        print(".")

def find_image(folder):
    for img in os.listdir(folder):
        if img.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_path = os.path.join(folder, img)
            try:
                img_coord = pyautogui.locateCenterOnScreen(full_path)
                logger.info(f"Imagem {img} encontrada na tela.")
                return img_coord
            except pyautogui.ImageNotFoundException:
                logger.warning(f"Imagem {img} não encontrada na tela.")
                continue
    return None

def read_files(folder_path):
    logger.info(f"Juntando todos os arquivos de grounding...")
    combined_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                combined_text += file.read() + "\n"
    return combined_text


def process_message(text, history):
    grounding = read_files(CONTENT_PATH)
    instruction = open("data/instructions/whatsapp-instruction.txt", "r").read()
    message = instruction + grounding + text
    logger.info(f"Enviando payload ao GPT...")
    result, history = querier.send_message(message, history)
    reply_message(result)
    return history


def reply_message(message):
    logger.info(f"Transmitindo resposta...")
    x4, y4 = [540, 1015]  # Caixa de entrada de texto
    pyautogui.moveTo(x4, y4)
    pyautogui.click()
    time.sleep(1)
    # pyautogui.typewrite(message, interval=0.01)
    pyperclip.copy(message)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    logger.info(f"Sucesso.")


if __name__ == "__main__":
    open_interface()
