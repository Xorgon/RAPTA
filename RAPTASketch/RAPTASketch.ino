#include <Arduino.h>
#include "ECU.h"
#include "MagEncoder.h"
#include "PXComms.h"

ECU ecu;
MagEncoder aoaSensor;
PXComms pixhawk;

ecu_response_t resp;
char output[500];

void setup() {
    Serial.begin(9600);
    ecu = ECU(Serial1);
    pixhawk = PXComms(Serial2);
    aoaSensor = MagEncoder(4, 7, 8);
    pixhawk.send_data_request();
}

void loop() {
    float angle = aoaSensor.getAngle();
    ecu.updateAll();

    sprintf(output, "%s, %s, %lu",
            String(pixhawk.get_airspeed()).c_str(),
            String(pixhawk.get_altitude()).c_str(),
            ecu.data.rpm
    );
    Serial.println(output);
}

void serialEvent2() {
    pixhawk.receive_data();
}