# TODO: Add file logging.

import serial
import serial.tools.list_ports as list_ports
import re
import ctypes

from PyQt5 import QtGui, QtWidgets, QtCore
import sys
import WindTunnelGUI


class WindTunnelGUIApp(QtWidgets.QMainWindow, WindTunnelGUI.Ui_MainWindow):
    ser = None
    ser_timer = None

    millis = None
    ias = None
    aoa = None
    bat_pct = None
    config_num = None
    aileron_config_label = None
    port_tail_config_label = None
    stbd_tail_config_label = None
    flap_config_label = None

    total_packets = 0
    bad_packets = 0

    def __init__(self, parent=None):
        super(WindTunnelGUIApp, self).__init__(parent)
        self.setupUi(self)

        # Reset the App ID to interact more nicely with Windows (separate icon from generic Python etc.).
        myappid = u'WindTunnelGUI'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.openDialog()
        # self.startSerial(com_port)

    def read_serial(self):
        if not self.ser.is_open:
            self.statusbar.showMessage("Serial port is not open")
            return
        self.total_packets += 1
        bad_packet_msg = "Received bad packet"
        line = self.ser.readline().strip().decode('utf-8')
        split = line.strip("~").split(",")
        if len(split) == 9 and line[-1] == "~":
            self.millis, \
            self.ias, \
            self.aoa, \
            self.bat_pct, \
            self.config_num, \
            self.aileron_config_label, \
            self.port_tail_config_label, \
            self.stbd_tail_config_label, \
            self.flap_config_label = split

            self.set_display_nums()
            self.statusbar.showMessage(line)
        else:
            self.bad_packets += 1
            print(100 * self.bad_packets / self.total_packets)
            self.statusbar.showMessage(bad_packet_msg + ": " + line)

    def set_display_nums(self):
        try:
            seconds = int(self.millis) / 1000
        except ValueError:
            seconds = 0
        self.tplus_number.display("{0:.2f}".format(seconds))
        self.ias_number.display(self.ias)
        self.bat_pct_number.display(self.bat_pct)
        self.aoa_number.display(self.aoa)
        self.config_label.setText(self.config_num)
        self.aileron_config.setText(self.aileron_config_label)
        self.port_tail_config.setText(self.port_tail_config_label)
        self.stbd_tail_config.setText(self.stbd_tail_config_label)
        self.flap_config.setText(self.flap_config_label)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
        super().closeEvent(a0)

    def openDialog(self):
        text, ok = QtWidgets.QInputDialog.getItem(self, 'COM Port',
                                                  'Select COM Port', [p.description for p in list_ports.comports()])

        if ok:
            port = re.findall("(COM\d+)", str(text))[-1]
            self.startSerial(port)

    def startSerial(self, com_port):
        self.ser = serial.Serial(com_port, baudrate=57600)
        self.ser_timer = QtCore.QTimer()
        self.ser_timer.setInterval(10)
        self.ser_timer.timeout.connect(self.read_serial)
        self.ser_timer.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = WindTunnelGUIApp()
    gui.show()
    app.exec_()
