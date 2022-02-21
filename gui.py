import configparser
import ast
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QPushButton, QApplication, QHBoxLayout, QWidget, QMainWindow
from key_presser import KeyPresser

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.widget = Gui()
        self.resize(500,100)
        self.move(100,100)
        self.setWindowTitle('Anti-Disco')
        # self.setWindowIcon(QtGui.QIcon('icon.ico')) Will be added.
        self.setCentralWidget(self.widget)

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        self.widget._stop()
        event.accept()

class Gui(QWidget):
    def __init__(self):
        super(Gui, self).__init__()
        self.init_gui()
        self.key_presser = None
        
    def init_gui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.load_config()
        self.load_button()

    def load_button(self):
        self.start = QPushButton('Start')
        self.start.clicked.connect(self._start)
        self.stop = QPushButton('Stop')
        self.stop.clicked.connect(self._stop)
        self.layout.addWidget(self.start)
        self.layout.addWidget(self.stop)


    def load_config(self):
        parser = configparser.ConfigParser()
        parser.read('anti-disco.config')
        self.sleep_duration = parser.getint('DEFAULT', 'sleep_duration', fallback=300)
        self.press_duration = parser.getfloat('DEFAULT', 'press_duration', fallback=1)
        self.keymap = ast.literal_eval(parser.get('DEFAULT', 'keymap', fallback='[w,s,a,d]'))


    def _start(self):
        if self.key_presser is not None:
            self.key_presser.shutdown_flag.set()
        self.key_presser = KeyPresser(self.sleep_duration, self.press_duration, self.keymap)
        self.key_presser.start()

    def _stop(self):
        if self.key_presser is not None:
            self.key_presser.shutdown_flag.set()

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
