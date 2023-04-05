# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'New_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import os 
import time 
import threading
import numpy as np
import time 
import os 
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.uic import loadUi
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1121, 854)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Centre_Widgets = QtWidgets.QGroupBox(self.centralwidget)
        self.Centre_Widgets.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(9)
        sizePolicy.setVerticalStretch(9)
        sizePolicy.setHeightForWidth(self.Centre_Widgets.sizePolicy().hasHeightForWidth())
        self.Centre_Widgets.setSizePolicy(sizePolicy)
        self.Centre_Widgets.setMinimumSize(QtCore.QSize(731, 781))
        self.Centre_Widgets.setObjectName("Centre_Widgets")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Centre_Widgets)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.camfeed1 = QtWidgets.QLabel(self.Centre_Widgets)
        self.camfeed1.setObjectName("camfeed1")
        self.horizontalLayout.addWidget(self.camfeed1)
        spacerItem = QtWidgets.QSpacerItem(15, 15, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.camfeed2 = QtWidgets.QLabel(self.Centre_Widgets)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camfeed2.sizePolicy().hasHeightForWidth())
        self.camfeed2.setSizePolicy(sizePolicy)
        self.camfeed2.setObjectName("camfeed2")
        self.horizontalLayout.addWidget(self.camfeed2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(1, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.imgcam1 = QtWidgets.QLabel(self.Centre_Widgets)
        self.imgcam1.setObjectName("imgcam1")
        self.horizontalLayout_2.addWidget(self.imgcam1)
        spacerItem2 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.GUI_Controls = QtWidgets.QGroupBox(self.Centre_Widgets)
        self.GUI_Controls.setMinimumSize(QtCore.QSize(25, 25))
        self.GUI_Controls.setAlignment(QtCore.Qt.AlignCenter)
        self.GUI_Controls.setObjectName("GUI_Controls")
        self.gridLayout = QtWidgets.QGridLayout(self.GUI_Controls)
        self.gridLayout.setObjectName("gridLayout")
        self.cam1_on = QtWidgets.QPushButton(self.GUI_Controls)
        self.cam1_on.setObjectName("cam1_on")
        self.gridLayout.addWidget(self.cam1_on, 0, 0, 1, 1)
        self.cam2_on = QtWidgets.QPushButton(self.GUI_Controls)
        self.cam2_on.setObjectName("cam2_on")
        self.gridLayout.addWidget(self.cam2_on, 0, 1, 1, 1)
        self.cam2_off = QtWidgets.QPushButton(self.GUI_Controls)
        self.cam2_off.setObjectName("cam2_off")
        self.gridLayout.addWidget(self.cam2_off, 2, 1, 1, 1)
        self.ip_off = QtWidgets.QPushButton(self.GUI_Controls)
        self.ip_off.setObjectName("ip_off")
        self.gridLayout.addWidget(self.ip_off, 7, 1, 1, 1)
        self.img1_off = QtWidgets.QPushButton(self.GUI_Controls)
        self.img1_off.setObjectName("img1_off")
        self.gridLayout.addWidget(self.img1_off, 4, 0, 1, 1)
        self.cam1_off = QtWidgets.QPushButton(self.GUI_Controls)
        self.cam1_off.setObjectName("cam1_off")
        self.gridLayout.addWidget(self.cam1_off, 2, 0, 1, 1)
        self.img1_on = QtWidgets.QPushButton(self.GUI_Controls)
        self.img1_on.setObjectName("img1_on")
        self.gridLayout.addWidget(self.img1_on, 3, 0, 1, 1)
        self.img2_off = QtWidgets.QPushButton(self.GUI_Controls)
        self.img2_off.setObjectName("img2_off")
        self.gridLayout.addWidget(self.img2_off, 4, 1, 1, 1)
        self.af_on = QtWidgets.QPushButton(self.GUI_Controls)
        self.af_on.setObjectName("af_on")
        self.gridLayout.addWidget(self.af_on, 5, 0, 1, 1)
        self.img2_on = QtWidgets.QPushButton(self.GUI_Controls)
        self.img2_on.setObjectName("img2_on")
        self.gridLayout.addWidget(self.img2_on, 3, 1, 1, 1)
        self.ip_on = QtWidgets.QPushButton(self.GUI_Controls)
        self.ip_on.setObjectName("ip_on")
        self.gridLayout.addWidget(self.ip_on, 5, 1, 1, 1)
        self.af_off = QtWidgets.QPushButton(self.GUI_Controls)
        self.af_off.setObjectName("af_off")
        self.gridLayout.addWidget(self.af_off, 7, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.GUI_Controls)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.imgcam2 = QtWidgets.QLabel(self.Centre_Widgets)
        self.imgcam2.setObjectName("imgcam2")
        self.horizontalLayout_2.addWidget(self.imgcam2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addWidget(self.Centre_Widgets, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MIP Graphical User Inteface "))
        self.camfeed1.setText(_translate("MainWindow", "Camera Feed 1 "))
        self.camfeed2.setText(_translate("MainWindow", "Camera Feed 2 "))
        self.imgcam1.setText(_translate("MainWindow", "Image 1"))
        self.GUI_Controls.setTitle(_translate("MainWindow", "GUI Controls "))
        self.cam1_on.setText(_translate("MainWindow", "Cam 1 On"))
        self.cam2_on.setText(_translate("MainWindow", "Cam 2 On"))
        self.cam2_off.setText(_translate("MainWindow", "Cam 2 Off"))
        self.ip_off.setText(_translate("MainWindow", "Close Window "))
        self.img1_off.setText(_translate("MainWindow", "Clear Cam 1 Image"))
        self.cam1_off.setText(_translate("MainWindow", "Cam 1 Off"))
        self.img1_on.setText(_translate("MainWindow", "Capture Cam 1 Image"))
        self.img2_off.setText(_translate("MainWindow", "Clear Cam 2 Image"))
        self.af_on.setText(_translate("MainWindow", "Enable Autofocus"))
        self.img2_on.setText(_translate("MainWindow", "Capture Cam 2 Image"))
        self.ip_on.setText(_translate("MainWindow", "Processing Window"))
        self.af_off.setText(_translate("MainWindow", "Disable Autofocus"))
        self.imgcam2.setText(_translate("MainWindow", "Image 2"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

