#include <Arduino.h>
#include "Servo.h"
#include "ECU.h"
#include "MagEncoder.h"
#include "PXComms.h"

#define rssiPin A0

ECU ecu;
MagEncoder aoaSensor;
PXComms pixhawk;

ecu_response_t resp;
char output[500];

void setup() {
    Serial.begin(57600);
    ecu = ECU(Serial1);
    pixhawk = PXComms(Serial2);
    aoaSensor = MagEncoder(4, 7, 8);
    pixhawk.send_data_request();
}

void loop() {
    float angle = aoaSensor.getAngle();
    ecu.updateAll();
    pixhawk.receive_data();
    float rssi = 100 * (analogRead(rssiPin) * 5.0 / 3.3) / 1024;
    sprintf(output, "%lu,%s,%s,%lu,%u,%s,%s,%u,%s,%s,%s,%i~",
            millis(),
            String(pixhawk.get_airspeed()).c_str(),
            String(pixhawk.get_altitude()).c_str(),
            ecu.data.rpm,
            ecu.data.egt,
            String(ecu.data.pumpPower).c_str(),
            String(ecu.data.batVoltage).c_str(),
            ecu.data.throttlePct,
            String(angle).c_str(),
            ecu.status.c_str(),
            String(rssi).c_str(),
            pixhawk.get_battery_pcnt()
    );
    Serial.println(output);
    delay(50);
}
