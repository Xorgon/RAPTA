#include <Arduino.h>
#include "ECU.h"

ECU ecu;

void setup() {
    ecu = ECU(Serial1);
    Serial.begin(9600);
    Serial.println("Initialized");
//    Serial1.begin(9600);
}

void loop() {
//    Serial1.write(0xC7);  // Sync
//    Serial1.write(0x2C);  // Sep
//    Serial1.write('R');  // R
//    Serial1.write('C');  // S
//    Serial1.write('V');  // D
//    Serial1.write(0x2C);  // Sep
//    Serial1.write(0x0D);  // CR
//    char to_print[16];
//    if (Serial1.available()) {
//        sprintf(to_print, "%x", Serial1.read());
//        Serial.println(to_print);
//        Serial.write(Serial1.read());
//    }
//      Serial.write(Serial1.read());
    Serial.println("Looping...");
    ecu.sendCommand("RCV");
    Serial.println(ecu.readResponse(Serial));
}
