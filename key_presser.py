import pyautogui
import random
import time
import threading

class KeyPresser(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.config = config
        random.seed(None)
        self.shutdown_flag = threading.Event()

    def press_random_key(self):
        choice = random.randint(0, len(self.config.keymap)-1)
        pyautogui.keyDown(self.config.keymap[choice])
        time.sleep(self.config.press_duration)
        pyautogui.keyUp(self.config.keymap[choice])

    def run(self):
        time.sleep(2)
        while not self.shutdown_flag.is_set():
            self.press_random_key()
            time.sleep(self.config.sleep_duration)

