import time
import os
import pyautogui
import pyperclip
import querier
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="./logs/log.txt",
    encoding="utf-8",
    format="%(asctime)s %(message)s",
)

APP_LINK = r"C:\Users\Patrick\Desktop\WhatsApp.lnk"
CONTENT_PATH = "./data/downloaded"
IMAGE_PATH = "./assets/copy-icon-3.png"


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
    reference_image = IMAGE_PATH
    placeholder = ""
    while True:
        time.sleep(5)
        x1, y1 = [235, 195]  # Último contato
        #x2, y2 = [
        #    1605,
        #    953,
        #]  # Última mensagem (Apenas durante os testes / automensagem)
        x2, y2 = [675,947] # Última mensagem

        pyautogui.moveTo(x1, y1)
        pyautogui.doubleClick()
        time.sleep(1)
        pyautogui.moveTo(x2, y2)
        pyautogui.rightClick()
        time.sleep(1)
        try:
            img_coord = pyautogui.locateCenterOnScreen(reference_image)
            pyautogui.moveTo(img_coord)
        except pyautogui.ImageNotFoundException:
            logging.error(
                f"Image not found, check if message is of text format or screen is correctly setup."
            )
            continue
        time.sleep(1)
        pyautogui.doubleClick()
        time.sleep(1)
        text = pyperclip.paste()

        if placeholder != text:
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
    instruction = open("data/instructions/whatsapp-instruction.txt", "r").read()
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
    # pyautogui.typewrite(message, interval=0.01)
    pyperclip.copy(message)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    logging.info(f"Sucesso.")


if __name__ == "__main__":
    open_interface()
