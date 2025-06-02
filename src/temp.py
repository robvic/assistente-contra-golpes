import pyautogui
import time

print("Move your mouse to the target position...")
time.sleep(5)  # Gives you 5 seconds to place the mouse

x, y = pyautogui.position()
print(f"Current mouse position: X={x}, Y={y}")
