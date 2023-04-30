import configparser
import ast

class Config_Object():
    def __init__(self, sleep_duration, press_duration, keymap):
        self.sleep_duration = sleep_duration
        self.press_duration = press_duration
        self.keymap = keymap

    def load_config(filename):
        parser = configparser.ConfigParser()
        parser.read(filename)
        sleep_duration = parser.getint('CONFIG', 'sleep_duration', fallback=300)
        press_duration = parser.getfloat('CONFIG', 'press_duration', fallback=1)
        keymap = ast.literal_eval(parser.get('CONFIG', 'keymap', fallback='[w,s,a,d]'))
        return Config_Object(sleep_duration, press_duration, keymap)
