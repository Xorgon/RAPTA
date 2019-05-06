# TODO: Add file logging.

import serial
import serial.tools.list_ports as list_ports
import re
import ctypes
import datetime
import struct
import math

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
    eng_bat_voltage = None
    throttle_pct = None
    aoa = None
    pitch = None
    eng_status = None
    rssi = None
    px_bat_voltage = None
    load_cell = None
    drag = None
    fuel_pct = None
    gps_sats = None

    total_packets = 0
    bad_packets = 0
    packet_loss = 0

    init_remote_time = None
    init_local_time = None

    dump_file = None

    def __init__(self, parent=None):
        super(TelemGUIApp, self).__init__(parent)
        self.setupUi(self)

        # Reset the App ID to interact more nicely with Windows (separate icon from generic Python etc.).
        myappid = u'TelemGUI'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.dump_file = open("telem_dump.log", "a")

        self.openDialog()
        # self.startSerial(com_port)

    def read_serial(self):
        if not self.ser.is_open:
            self.statusbar.showMessage("Serial port is not open")
            return
        self.total_packets += 1
        sync_bytes = 0
        this_byte = None
        print("Reading packet...")
        while this_byte is None or this_byte != b'\xC7':
            this_byte = self.ser.read(1)
            try:
                print(this_byte.decode('utf-8'), end='')
            except UnicodeDecodeError:
                print(this_byte)
        print("Reading sync bytes...")
        while this_byte == b'\xC7':
            sync_bytes += 1
            this_byte = self.ser.read(1)
        packet = this_byte + self.ser.read(82)  # 83
        self.dump_file.write(str(packet) + "\n")
        if sync_bytes == 3:
            self.millis, \
            self.ias, \
            self.alt, \
            self.rpm, \
            self.egt, \
            self.pump_power, \
            self.eng_bat_voltage, \
            self.throttle_pct, \
            self.aoa, \
            self.pitch, \
            self.eng_status, \
            self.rssi, \
            self.px_bat_voltage, \
            self.load_cell, \
            self.drag, \
            self.fuel_pct = struct.unpack('=LffLHffBff33sfHffb', packet)

            self.set_display_nums()
            self.statusbar.showMessage("Packet received successfully")
            if self.init_remote_time is None:
                self.init_remote_time = float(self.millis) / 1000
                self.init_local_time = datetime.datetime.now()
            else:
                remote_delta = float(self.millis) / 1000 - self.init_remote_time
                local_delta = (datetime.datetime.now() - self.init_local_time).total_seconds()
                delta_diff = remote_delta - local_delta
                print(delta_diff)
        else:
            self.bad_packets += 1
            bad_packet_msg = "Received bad packet (" + str(self.bad_packets) + "," + str(sync_bytes) + ")"
            self.statusbar.showMessage(bad_packet_msg)
            # self.ser.flush()
            self.packet_loss_number.display("{:3.2f}".format(self.packet_loss))
            print("--------------")
            for b in packet:
                print("%02X" % (b))
        self.packet_loss = 100 * self.bad_packets / self.total_packets

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
        self.bat_voltage_number.display(self.eng_bat_voltage)
        self.throttle_pct_number.display(self.throttle_pct)
        self.alt_number.display(self.alt)
        self.aoa_number.display(self.aoa)
        self.pitch_number.display(math.degrees(self.pitch))
        self.eng_status_box.setText(self.eng_status.decode('utf-8'))
        self.packet_loss_number.display("{:3.2f}".format(self.packet_loss))
        self.rssi_number.display(self.rssi)
        self.px_bat_voltage_number.display("{:.2f}".format(float(self.px_bat_voltage) / 1000))
        self.load_cell_number.display(self.load_cell)
        self.drag_number.display(self.drag)
        self.fuel_pct_number.display(abs(self.fuel_pct))
        if self.fuel_pct > 0:
            self.fuel_pct_number.setStyleSheet("background-color: #aaffaa")
        else:
            self.fuel_pct_number.setStyleSheet("background-color: #ffaaaa")

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
    gui = TelemGUIApp()
    gui.show()
    app.exec_()
