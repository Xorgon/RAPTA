# TODO: Add file logging.

import serial
import serial.tools.list_ports as list_ports
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

    def __init__(self, com_port, parent=None):
        super(TelemGUIApp, self).__init__(parent)
        self.setupUi(self)

        # Reset the App ID to interact more nicely with Windows (separate icon from generic Python etc.).
        myappid = u'TelemGUI'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.openDialog()
        # self.startSerial(com_port)

    def read_serial(self):
        if not self.ser.is_open:
            self.statusbar.showMessage("Serial port is not open")
            return
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
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
        super().closeEvent(a0)

    def openDialog(self):
        text, ok = QtWidgets.QInputDialog.getItem(self, 'COM Port',
                                                  'Select COM Port', [p.device for p in list_ports.comports()])

        if ok:
            self.startSerial(str(text))

    def startSerial(self, com_port):
        self.ser = serial.Serial(com_port)
        self.ser_timer = QtCore.QTimer()
        self.ser_timer.setInterval(10)
        self.ser_timer.timeout.connect(self.read_serial)
        self.ser_timer.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = TelemGUIApp("COM7")
    gui.show()
    app.exec_()
