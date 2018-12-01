#include <Arduino.h>
#include "ECU.h"

ECU ecu;

void setup() {
    ecu = ECU(Serial1);
    Serial.begin(9600);
}

void loop() {
    Serial.println(ecu.readCurrentValues());
}