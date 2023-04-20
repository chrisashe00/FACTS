#V0 - GUI shell Only
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi('qt_gui.ui', self)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    dark(app)
    modern_window = ModernWindow(window)
    modern_window.show()
    sys.exit(app.exec_())