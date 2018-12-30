# TODO: Add file logging.

import serial
import ctypes

from PyQt5 import QtGui, QtWidgets, QtCore
import sys
import TelemGUI


class TelemGUIApp(QtWidgets.QMainWindow, TelemGUI.Ui_MainWindow):
    ser = None
    ser_timer = None

    millis = None
    ias = None
    alt = None
    rpm = None
    egt = None
    pump_power = None
    bat_voltage = None
    throttle_pct = None
    aoa = None
    eng_status = None

    def __init__(self, parent=None):
        super(TelemGUIApp, self).__init__(parent)
        self.setupUi(self)

        # Reset the App ID to interact more nicely with Windows (separate icon from generic Python etc.).
        myappid = u'TelemGUI'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.ser = serial.Serial('COM7')
        self.ser_timer = QtCore.QTimer()
        self.ser_timer.setInterval(10)
        self.ser_timer.timeout.connect(self.read_serial)
        self.ser_timer.start()

    def read_serial(self):
        bad_packet_msg = "Received bad packet"
        line = self.ser.readline().strip().decode('utf-8')
        split = line.split(",")
        if len(split) == 10:
            self.millis, \
            self.ias, \
            self.alt, \
            self.rpm, \
            self.egt, \
            self.pump_power, \
            self.bat_voltage, \
            self.throttle_pct, \
            self.aoa, \
            self.eng_status = split

            self.set_display_nums()
            self.statusbar.showMessage(line)
        else:
            self.statusbar.showMessage(bad_packet_msg + ": " + line)

    def set_display_nums(self):
        try:
            seconds = int(self.millis) / 1000
        except ValueError:
            seconds = 0
        self.tplus_number.display("{0:.2f}".format(seconds))
        self.ias_number.display(self.ias)
        self.rpm_number.display(self.rpm)
        self.egt_number.display(self.egt)
        self.pump_power_number.display(self.pump_power)
        self.bat_voltage_number.display(self.bat_voltage)
        self.throttle_pct_number.display(self.throttle_pct)
        self.alt_number.display(self.alt)
        self.aoa_number.display(self.aoa)
        self.eng_status_box.setText(self.eng_status)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ser.close()
        super().closeEvent(a0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = TelemGUIApp()
    gui.show()
    app.exec_()
