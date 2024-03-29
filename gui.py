import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QPushButton, QApplication, QHBoxLayout, QWidget, QMainWindow, QComboBox, QAction
from os import listdir
from os.path import isfile, join
from config_object import Config_Object
from key_presser import KeyPresser


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.widget = Gui()
        self.resize(500,100)
        self.move(100,100)
        self.setWindowTitle('Anti-Disco')
        menu_bar = self.menuBar()
        config_menu = menu_bar.addMenu('&Konfiguration')
        new_config = QAction('&Neu', self)
        new_config.setStatusTip('Legt eine neue Konfiguration an.')
        new_config.setShortcut('Ctrl+N')
        new_config.triggered.connect(self.new_configuration)
        config_menu.addAction(new_config)
        self.setCentralWidget(self.widget)

    def closeEvent(self, event):
        self.widget._stop()
        event.accept()

    def new_configuration(self, s):
        print(f'new config')

class Gui(QWidget):
    def __init__(self):
        super(Gui, self).__init__()
        self.init_gui()
        self.key_presser = None
        
    def init_gui(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.config_folder = 'config'
        self.filename = 'default'
        self.configs = {}
        self.load_configs()
        self.load_button()

    def load_button(self):
        self.start = QPushButton('Start')
        self.start.clicked.connect(self._start)
        self.stop = QPushButton('Stop')
        self.stop.clicked.connect(self._stop)
        self.layout.addWidget(self.start)
        self.layout.addWidget(self.stop)


    def load_configs(self):
        self.config = QComboBox()
        self.config.currentTextChanged.connect(self._change_config)
        self.layout.addWidget(self.config)
        config_files = [f for f in listdir(self.config_folder) if isfile(join(self.config_folder, f))]
        for file in config_files:
            self.add_config(file)


    def add_config(self, name):
        self.configs.update({name : Config_Object.load_config(f'{self.config_folder}/{name}') })
        self.config.addItem(name)


    def _change_config(self, name):
        self.filename = name

    def _start(self):
        if self.key_presser is not None:
            self.key_presser.shutdown_flag.set()
        
        self.key_presser = KeyPresser(self.configs[self.filename])
        self.key_presser.start()

    def _stop(self):
        if self.key_presser is not None:
            self.key_presser.shutdown_flag.set()

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
