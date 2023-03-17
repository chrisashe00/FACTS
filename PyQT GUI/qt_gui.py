from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1040, 824)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Left_Widgets = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Left_Widgets.sizePolicy().hasHeightForWidth())
        self.Left_Widgets.setSizePolicy(sizePolicy)
        self.Left_Widgets.setMinimumSize(QtCore.QSize(141, 781))
        self.Left_Widgets.setObjectName("Left_Widgets")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Left_Widgets)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cam1_on = QtWidgets.QPushButton(self.Left_Widgets)
        self.cam1_on.setObjectName("cam1_on")
        self.verticalLayout.addWidget(self.cam1_on)
        self.cam1_off = QtWidgets.QPushButton(self.Left_Widgets)
        self.cam1_off.setObjectName("cam1_off")
        self.verticalLayout.addWidget(self.cam1_off)
        self.cam1_bri_label = QtWidgets.QLabel(self.Left_Widgets)
        self.cam1_bri_label.setMaximumSize(QtCore.QSize(121, 28))
        self.cam1_bri_label.setObjectName("cam1_bri_label")
        self.verticalLayout.addWidget(self.cam1_bri_label)
        self.cam1_bri_slider = QtWidgets.QSlider(self.Left_Widgets)
        self.cam1_bri_slider.setOrientation(QtCore.Qt.Horizontal)
        self.cam1_bri_slider.setObjectName("cam1_bri_slider")
        self.verticalLayout.addWidget(self.cam1_bri_slider)
        self.cam1_con_label = QtWidgets.QLabel(self.Left_Widgets)
        self.cam1_con_label.setMaximumSize(QtCore.QSize(121, 28))
        self.cam1_con_label.setObjectName("cam1_con_label")
        self.verticalLayout.addWidget(self.cam1_con_label)
        self.cam1_con_slider = QtWidgets.QSlider(self.Left_Widgets)
        self.cam1_con_slider.setOrientation(QtCore.Qt.Horizontal)
        self.cam1_con_slider.setObjectName("cam1_con_slider")
        self.verticalLayout.addWidget(self.cam1_con_slider)
        self.cam1_denoise = QtWidgets.QPushButton(self.Left_Widgets)
        self.cam1_denoise.setObjectName("cam1_denoise")
        self.verticalLayout.addWidget(self.cam1_denoise)
        self.img1_takeimg = QtWidgets.QPushButton(self.Left_Widgets)
        self.img1_takeimg.setObjectName("img1_takeimg")
        self.verticalLayout.addWidget(self.img1_takeimg)
        self.img1_bri_label = QtWidgets.QLabel(self.Left_Widgets)
        self.img1_bri_label.setMaximumSize(QtCore.QSize(121, 28))
        self.img1_bri_label.setObjectName("img1_bri_label")
        self.verticalLayout.addWidget(self.img1_bri_label)
        self.img1_bri_slider = QtWidgets.QSlider(self.Left_Widgets)
        self.img1_bri_slider.setOrientation(QtCore.Qt.Horizontal)
        self.img1_bri_slider.setObjectName("img1_bri_slider")
        self.verticalLayout.addWidget(self.img1_bri_slider)
        self.img1_con_label = QtWidgets.QLabel(self.Left_Widgets)
        self.img1_con_label.setMaximumSize(QtCore.QSize(121, 28))
        self.img1_con_label.setObjectName("img1_con_label")
        self.verticalLayout.addWidget(self.img1_con_label)
        self.img1_con_slider = QtWidgets.QSlider(self.Left_Widgets)
        self.img1_con_slider.setOrientation(QtCore.Qt.Horizontal)
        self.img1_con_slider.setObjectName("img1_con_slider")
        self.verticalLayout.addWidget(self.img1_con_slider)
        self.img1_denoise = QtWidgets.QPushButton(self.Left_Widgets)
        self.img1_denoise.setObjectName("img1_denoise")
        self.verticalLayout.addWidget(self.img1_denoise)
        self.autofocus_on = QtWidgets.QPushButton(self.Left_Widgets)
        self.autofocus_on.setObjectName("autofocus_on")
        self.verticalLayout.addWidget(self.autofocus_on)
        self.autofocus_off = QtWidgets.QPushButton(self.Left_Widgets)
        self.autofocus_off.setObjectName("autofocus_off")
        self.verticalLayout.addWidget(self.autofocus_off)
        self.gridLayout_2.addWidget(self.Left_Widgets, 0, 0, 1, 1)
        self.Centre_Widgets = QtWidgets.QGroupBox(self.centralwidget)
        self.Centre_Widgets.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(9)
        sizePolicy.setVerticalStretch(9)
        sizePolicy.setHeightForWidth(self.Centre_Widgets.sizePolicy().hasHeightForWidth())
        self.Centre_Widgets.setSizePolicy(sizePolicy)
        self.Centre_Widgets.setMinimumSize(QtCore.QSize(731, 781))
        self.Centre_Widgets.setObjectName("Centre_Widgets")
        self.gridLayout = QtWidgets.QGridLayout(self.Centre_Widgets)
        self.gridLayout.setObjectName("gridLayout")
        self.imgcam1 = QtWidgets.QLabel(self.Centre_Widgets)
        self.imgcam1.setObjectName("imgcam1")
        self.gridLayout.addWidget(self.imgcam1, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.camfeed2 = QtWidgets.QLabel(self.Centre_Widgets)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.camfeed2.sizePolicy().hasHeightForWidth())
        self.camfeed2.setSizePolicy(sizePolicy)
        self.camfeed2.setObjectName("camfeed2")
        self.gridLayout.addWidget(self.camfeed2, 0, 2, 1, 1)
        self.imgcam2 = QtWidgets.QLabel(self.Centre_Widgets)
        self.imgcam2.setObjectName("imgcam2")
        self.gridLayout.addWidget(self.imgcam2, 2, 2, 1, 1)
        self.camfeed1 = QtWidgets.QLabel(self.Centre_Widgets)
        self.camfeed1.setObjectName("camfeed1")
        self.gridLayout.addWidget(self.camfeed1, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.Centre_Widgets, 0, 1, 1, 1)
        self.Right_Widgets = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Right_Widgets.sizePolicy().hasHeightForWidth())
        self.Right_Widgets.setSizePolicy(sizePolicy)
        self.Right_Widgets.setMinimumSize(QtCore.QSize(141, 781))
        self.Right_Widgets.setObjectName("Right_Widgets")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Right_Widgets)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_8 = QtWidgets.QPushButton(self.Right_Widgets)
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_2.addWidget(self.pushButton_8)
        self.pushButton_9 = QtWidgets.QPushButton(self.Right_Widgets)
        self.pushButton_9.setObjectName("pushButton_9")
        self.verticalLayout_2.addWidget(self.pushButton_9)
        self.cam2_bri_label = QtWidgets.QLabel(self.Right_Widgets)
        self.cam2_bri_label.setMaximumSize(QtCore.QSize(121, 28))
        self.cam2_bri_label.setObjectName("cam2_bri_label")
        self.verticalLayout_2.addWidget(self.cam2_bri_label)
        self.cam2_bri_slider = QtWidgets.QSlider(self.Right_Widgets)
        self.cam2_bri_slider.setOrientation(QtCore.Qt.Horizontal)
        self.cam2_bri_slider.setObjectName("cam2_bri_slider")
        self.verticalLayout_2.addWidget(self.cam2_bri_slider)
        self.cam2_con_label = QtWidgets.QLabel(self.Right_Widgets)
        self.cam2_con_label.setMaximumSize(QtCore.QSize(121, 28))
        self.cam2_con_label.setObjectName("cam2_con_label")
        self.verticalLayout_2.addWidget(self.cam2_con_label)
        self.cam2_con_slider = QtWidgets.QSlider(self.Right_Widgets)
        self.cam2_con_slider.setOrientation(QtCore.Qt.Horizontal)
        self.cam2_con_slider.setObjectName("cam2_con_slider")
        self.verticalLayout_2.addWidget(self.cam2_con_slider)
        self.pushButton_10 = QtWidgets.QPushButton(self.Right_Widgets)
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout_2.addWidget(self.pushButton_10)
        self.pushButton_11 = QtWidgets.QPushButton(self.Right_Widgets)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout_2.addWidget(self.pushButton_11)
        self.im2_bri_label = QtWidgets.QLabel(self.Right_Widgets)
        self.im2_bri_label.setMaximumSize(QtCore.QSize(121, 28))
        self.im2_bri_label.setObjectName("im2_bri_label")
        self.verticalLayout_2.addWidget(self.im2_bri_label)
        self.img2_bri_slider = QtWidgets.QSlider(self.Right_Widgets)
        self.img2_bri_slider.setOrientation(QtCore.Qt.Horizontal)
        self.img2_bri_slider.setObjectName("img2_bri_slider")
        self.verticalLayout_2.addWidget(self.img2_bri_slider)
        self.img2_con_label = QtWidgets.QLabel(self.Right_Widgets)
        self.img2_con_label.setMaximumSize(QtCore.QSize(121, 28))
        self.img2_con_label.setObjectName("img2_con_label")
        self.verticalLayout_2.addWidget(self.img2_con_label)
        self.img2_con_slider = QtWidgets.QSlider(self.Right_Widgets)
        self.img2_con_slider.setOrientation(QtCore.Qt.Horizontal)
        self.img2_con_slider.setObjectName("img2_con_slider")
        self.verticalLayout_2.addWidget(self.img2_con_slider)
        self.pushButton_12 = QtWidgets.QPushButton(self.Right_Widgets)
        self.pushButton_12.setObjectName("pushButton_12")
        self.verticalLayout_2.addWidget(self.pushButton_12)
        self.xystg_pos_label = QtWidgets.QLabel(self.Right_Widgets)
        self.xystg_pos_label.setMaximumSize(QtCore.QSize(121, 28))
        self.xystg_pos_label.setObjectName("xystg_pos_label")
        self.verticalLayout_2.addWidget(self.xystg_pos_label)
        self.xystg_pos_value = QtWidgets.QLabel(self.Right_Widgets)
        self.xystg_pos_value.setMaximumSize(QtCore.QSize(121, 28))
        self.xystg_pos_value.setText("")
        self.xystg_pos_value.setObjectName("xystg_pos_value")
        self.verticalLayout_2.addWidget(self.xystg_pos_value)
        self.zstg_pos_label = QtWidgets.QLabel(self.Right_Widgets)
        self.zstg_pos_label.setMaximumSize(QtCore.QSize(121, 28))
        self.zstg_pos_label.setObjectName("zstg_pos_label")
        self.verticalLayout_2.addWidget(self.zstg_pos_label)
        self.zstg_pos_value = QtWidgets.QLabel(self.Right_Widgets)
        self.zstg_pos_value.setMaximumSize(QtCore.QSize(121, 28))
        self.zstg_pos_value.setText("")
        self.zstg_pos_value.setObjectName("zstg_pos_value")
        self.verticalLayout_2.addWidget(self.zstg_pos_value)
        self.gridLayout_2.addWidget(self.Right_Widgets, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Left_Widgets.setTitle(_translate("MainWindow", "Left Widget Column"))
        self.cam1_on.setText(_translate("MainWindow", "Camera 1 On"))
        self.cam1_off.setText(_translate("MainWindow", "Camera 1 Off"))
        self.cam1_bri_label.setText(_translate("MainWindow", "Brightness Camera 1"))
        self.cam1_con_label.setText(_translate("MainWindow", "Contrast Camera 1"))
        self.cam1_denoise.setText(_translate("MainWindow", "Denoise Camera 1"))
        self.img1_takeimg.setText(_translate("MainWindow", "Camera 1 Image"))
        self.img1_bri_label.setText(_translate("MainWindow", "Brightness Image 1"))
        self.img1_con_label.setText(_translate("MainWindow", "Contrast Image 1"))
        self.img1_denoise.setText(_translate("MainWindow", "Denoise Image 1"))
        self.autofocus_on.setText(_translate("MainWindow", "Enable Autofocus"))
        self.autofocus_off.setText(_translate("MainWindow", "Disable Autofocus"))
        self.imgcam1.setText(_translate("MainWindow", "Image 1"))
        self.camfeed2.setText(_translate("MainWindow", "Camera Feed 2 "))
        self.imgcam2.setText(_translate("MainWindow", "Image 2"))
        self.camfeed1.setText(_translate("MainWindow", "Camera Feed 1 "))
        self.Right_Widgets.setTitle(_translate("MainWindow", "Right Widget Column"))
        self.pushButton_8.setText(_translate("MainWindow", "Camera 2  On"))
        self.pushButton_9.setText(_translate("MainWindow", "Camera 2 Off"))
        self.cam2_bri_label.setText(_translate("MainWindow", "Brightness Camera 2"))
        self.cam2_con_label.setText(_translate("MainWindow", "Contrast Camera 2"))
        self.pushButton_10.setText(_translate("MainWindow", "Denoise Camera 2"))
        self.pushButton_11.setText(_translate("MainWindow", "Camera 2 Image"))
        self.im2_bri_label.setText(_translate("MainWindow", "Brightness Image 2"))
        self.img2_con_label.setText(_translate("MainWindow", "Contrast Image 2"))
        self.pushButton_12.setText(_translate("MainWindow", "Denoise Image 2"))
        self.xystg_pos_label.setText(_translate("MainWindow", "X-Y Stage Position"))
        self.zstg_pos_label.setText(_translate("MainWindow", "Z Stage Position"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())