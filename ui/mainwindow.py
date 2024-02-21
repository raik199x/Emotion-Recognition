from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow


from os import path

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()