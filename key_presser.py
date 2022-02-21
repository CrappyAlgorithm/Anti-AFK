import pyautogui
import random
import time
import threading

class KeyPresser(threading.Thread):
    def __init__(self, sleep_duration, press_duration, keymap):
        threading.Thread.__init__(self)
        self.sleep_duration = sleep_duration
        self.press_duration = press_duration
        self.keymap = keymap
        random.seed(None)
        self.shutdown_flag = threading.Event()

    def press_random_key(self):
        choice = random.randint(0, len(self.keymap)-1)
        pyautogui.keyDown(self.keymap[choice])
        time.sleep(self.press_duration)
        pyautogui.keyUp(self.keymap[choice])

    def run(self):
        time.sleep(2)
        while not self.shutdown_flag.is_set():
            self.press_random_key()
            time.sleep(self.sleep_duration)

