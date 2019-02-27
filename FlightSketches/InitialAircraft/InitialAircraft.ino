#include <Arduino.h>
#include "Servo.h"
#include "ECU.h"
#include "MagEncoder.h"
#include "PXComms.h"
#include "HX711.h"
#include "Logger.h"

#define rssiPin A0
#define edfBatPin A1
#define LOAD_CELL_DOUT  13
#define LOAD_CELL_CLK  12

MagEncoder aoaSensor;
PXComms pixhawk;
HX711 loadCell;
long loadCellReading;
Logger logger;

char output[500];

void setup() {
    Serial.begin(57600);
    pixhawk = PXComms(Serial2);
    aoaSensor = MagEncoder(4, 7, 8);
    loadCell.begin(LOAD_CELL_DOUT, LOAD_CELL_CLK);
    loadCellReading = 0;
    logger = Logger(5);
    pixhawk.send_data_request();
}

void loop() {
    float angle = aoaSensor.getAngle();
//    ecu.updateAll();
    pixhawk.receive_data();
    float rssi = 100 * (analogRead(rssiPin) * 4.8 / 3.3) / 1024;
    float batVoltage = 1.066 * 10.0 * 4.8 * analogRead(edfBatPin) / 1024.0;  // 1.066 is calibration factor
    if (loadCell.is_ready()) {
        loadCellReading = loadCell.read();
    }
    sprintf(output, "%lu,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%u,%s,%s,%s~",
            millis(),
            String(pixhawk.get_airspeed()).c_str(),
            String(pixhawk.get_altitude()).c_str(),
            "--", //ecu.data.rpm,
            "--", //ecu.data.egt,
            "--", //String(ecu.data.pumpPower).c_str(),
            String(batVoltage).c_str(), //String(ecu.data.batVoltage).c_str(),
            "--", //ecu.data.throttlePct,
            String(angle).c_str(),
            "----", //ecu.status.c_str(),
            String(rssi).c_str(),
            pixhawk.get_battery_mv(),
            String(loadCellReading).c_str(),
            String("--").c_str(),
            String(pixhawk.get_gps_sats()).c_str()
    );
    Serial.println(output);
    logger.log(output);
    delay(100);
}
