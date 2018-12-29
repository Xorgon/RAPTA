#include <Arduino.h>
#include "ECU.h"

ECU ecu;

void setup() {
    ecu = ECU(Serial1);
    Serial.begin(9600);
    Serial.println("Initialized");
}

void loop() {
    ecu.updateAll();
    Serial.println(ecu.status);
    Serial.println(ecu.data.rpm);
}
