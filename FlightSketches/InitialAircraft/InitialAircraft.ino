#include <Arduino.h>
#include "Servo.h"
#include "ECU.h"
#include "MagEncoder.h"
#include "PXComms.h"
#include "HX711.h"

#define rssiPin A0
#define LOAD_CELL_DOUT  13
#define LOAD_CELL_CLK  12

MagEncoder aoaSensor;
PXComms pixhawk;
HX711 loadCell;

char output[500];

void setup() {
    Serial.begin(57600);
    pixhawk = PXComms(Serial2);
    aoaSensor = MagEncoder(4, 7, 8);
    loadCell = HX711(LOAD_CELL_DOUT, LOAD_CELL_CLK);
    pixhawk.send_data_request();
}

void loop() {
    float angle = aoaSensor.getAngle();
//    ecu.updateAll();
    pixhawk.receive_data();
    float rssi = 100 * (analogRead(rssiPin) * 5.0 / 3.3) / 1024;
    sprintf(output, "%lu,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%u,%lu,%s~",
            millis(),
            String(pixhawk.get_airspeed()).c_str(),
            String(pixhawk.get_altitude()).c_str(),
            "--", //ecu.data.rpm,
            "--", //ecu.data.egt,
            "--", //String(ecu.data.pumpPower).c_str(),
            String(0.0).c_str(), //String(ecu.data.batVoltage).c_str(),
            "--", //ecu.data.throttlePct,
            String(angle).c_str(),
            "----", //ecu.status.c_str(),
            String(rssi).c_str(),
            pixhawk.get_battery_mv(),
            0,
            String("--").c_str()
    );
    Serial.println(output);
    delay(50);
}
