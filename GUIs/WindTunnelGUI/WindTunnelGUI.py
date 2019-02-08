# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WindTunnelGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(836, 377)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(836, 377))
        MainWindow.setMaximumSize(QtCore.QSize(836, 377))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(64, 64))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(130, 210, 592, 104))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.AircraftBox = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.AircraftBox.setContentsMargins(0, 0, 0, 0)
        self.AircraftBox.setObjectName("AircraftBox")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.AircraftBox.addWidget(self.label_2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tplus_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tplus_label.sizePolicy().hasHeightForWidth())
        self.tplus_label.setSizePolicy(sizePolicy)
        self.tplus_label.setMinimumSize(QtCore.QSize(0, 0))
        self.tplus_label.setBaseSize(QtCore.QSize(0, 0))
        self.tplus_label.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";")
        self.tplus_label.setObjectName("tplus_label")
        self.gridLayout_3.addWidget(self.tplus_label, 0, 0, 1, 1)
        self.aoa_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aoa_label.sizePolicy().hasHeightForWidth())
        self.aoa_label.setSizePolicy(sizePolicy)
        self.aoa_label.setMinimumSize(QtCore.QSize(0, 0))
        self.aoa_label.setBaseSize(QtCore.QSize(0, 0))
        self.aoa_label.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";")
        self.aoa_label.setObjectName("aoa_label")
        self.gridLayout_3.addWidget(self.aoa_label, 0, 2, 1, 1)
        self.ias_number = QtWidgets.QLCDNumber(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ias_number.sizePolicy().hasHeightForWidth())
        self.ias_number.setSizePolicy(sizePolicy)
        self.ias_number.setMinimumSize(QtCore.QSize(120, 40))
        self.ias_number.setDigitCount(6)
        self.ias_number.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.ias_number.setObjectName("ias_number")
        self.gridLayout_3.addWidget(self.ias_number, 1, 1, 1, 1)
        self.tplus_number = QtWidgets.QLCDNumber(self.verticalLayoutWidget_2)
        self.tplus_number.setMinimumSize(QtCore.QSize(100, 0))
        self.tplus_number.setDigitCount(7)
        self.tplus_number.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.tplus_number.setObjectName("tplus_number")
        self.gridLayout_3.addWidget(self.tplus_number, 1, 0, 1, 1)
        self.ias_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ias_label.sizePolicy().hasHeightForWidth())
        self.ias_label.setSizePolicy(sizePolicy)
        self.ias_label.setMinimumSize(QtCore.QSize(0, 0))
        self.ias_label.setBaseSize(QtCore.QSize(0, 0))
        self.ias_label.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";")
        self.ias_label.setObjectName("ias_label")
        self.gridLayout_3.addWidget(self.ias_label, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.aoa_number = QtWidgets.QLCDNumber(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aoa_number.sizePolicy().hasHeightForWidth())
        self.aoa_number.setSizePolicy(sizePolicy)
        self.aoa_number.setMinimumSize(QtCore.QSize(150, 40))
        self.aoa_number.setDigitCount(7)
        self.aoa_number.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.aoa_number.setObjectName("aoa_number")
        self.gridLayout_3.addWidget(self.aoa_number, 1, 2, 1, 1)
        self.bat_pct_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bat_pct_label.sizePolicy().hasHeightForWidth())
        self.bat_pct_label.setSizePolicy(sizePolicy)
        self.bat_pct_label.setMinimumSize(QtCore.QSize(0, 0))
        self.bat_pct_label.setBaseSize(QtCore.QSize(0, 0))
        self.bat_pct_label.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";")
        self.bat_pct_label.setObjectName("bat_pct_label")
        self.gridLayout_3.addWidget(self.bat_pct_label, 0, 3, 1, 1)
        self.bat_pct_number = QtWidgets.QLCDNumber(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bat_pct_number.sizePolicy().hasHeightForWidth())
        self.bat_pct_number.setSizePolicy(sizePolicy)
        self.bat_pct_number.setMinimumSize(QtCore.QSize(150, 40))
        self.bat_pct_number.setDigitCount(7)
        self.bat_pct_number.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.bat_pct_number.setObjectName("bat_pct_number")
        self.gridLayout_3.addWidget(self.bat_pct_number, 1, 3, 1, 1)
        self.AircraftBox.addLayout(self.gridLayout_3)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(180, 80, 502, 113))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.config_label = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.config_label.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.config_label.setFont(font)
        self.config_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.config_label.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";\n"
"border-color: rgb(172, 172, 172);\n"
"background-color: rgba(255, 255, 255, 0);\n"
"selection-color: rgb(122, 122, 122);")
        self.config_label.setInputMethodHints(QtCore.Qt.ImhNone)
        self.config_label.setObjectName("config_label")
        self.horizontalLayout.addWidget(self.config_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(120, 0))
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_8.setMinimumSize(QtCore.QSize(120, 0))
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(120, 0))
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_10.setMinimumSize(QtCore.QSize(120, 0))
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 0, 3, 1, 1)
        self.aileron_config = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.aileron_config.setMaximumSize(QtCore.QSize(16777215, 35))
        self.aileron_config.setFocusPolicy(QtCore.Qt.NoFocus)
        self.aileron_config.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";\n"
"border-color: rgb(172, 172, 172);\n"
"background-color: rgba(255, 255, 255, 0);\n"
"selection-color: rgb(122, 122, 122);")
        self.aileron_config.setObjectName("aileron_config")
        self.gridLayout.addWidget(self.aileron_config, 1, 0, 1, 1)
        self.port_tail_config = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.port_tail_config.setMaximumSize(QtCore.QSize(16777215, 35))
        self.port_tail_config.setFocusPolicy(QtCore.Qt.NoFocus)
        self.port_tail_config.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";\n"
"border-color: rgb(172, 172, 172);\n"
"background-color: rgba(255, 255, 255, 0);\n"
"selection-color: rgb(122, 122, 122);")
        self.port_tail_config.setObjectName("port_tail_config")
        self.gridLayout.addWidget(self.port_tail_config, 1, 1, 1, 1)
        self.stbd_tail_config = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.stbd_tail_config.setMaximumSize(QtCore.QSize(16777215, 35))
        self.stbd_tail_config.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stbd_tail_config.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";\n"
"border-color: rgb(172, 172, 172);\n"
"background-color: rgba(255, 255, 255, 0);\n"
"selection-color: rgb(122, 122, 122);")
        self.stbd_tail_config.setObjectName("stbd_tail_config")
        self.gridLayout.addWidget(self.stbd_tail_config, 1, 2, 1, 1)
        self.flap_config = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.flap_config.setMaximumSize(QtCore.QSize(16777215, 35))
        self.flap_config.setFocusPolicy(QtCore.Qt.NoFocus)
        self.flap_config.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";\n"
"border-color: rgb(172, 172, 172);\n"
"background-color: rgba(255, 255, 255, 0);\n"
"selection-color: rgb(122, 122, 122);")
        self.flap_config.setObjectName("flap_config")
        self.gridLayout.addWidget(self.flap_config, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 836, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RAPTA Telemetry"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Aircraft Data</span></p></body></html>"))
        self.tplus_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">T+</p></body></html>"))
        self.aoa_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">AoA</p></body></html>"))
        self.ias_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">IAS</p></body></html>"))
        self.bat_pct_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Bat %</p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Configuration</span></p></body></html>"))
        self.config_label.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Ailerons</span></p></body></html>"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Stbd Tail</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Port Tail</span></p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Flaps</span></p></body></html>"))
        self.aileron_config.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.port_tail_config.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.stbd_tail_config.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.flap_config.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

