#include <Arduino.h>
#include "ECU.h"

ECU ecu;

void setup() {
    ecu = ECU(8, 9);
    Serial.begin(9600);
}

void loop() {
    Serial.println(ecu.readCurrentValues());
}