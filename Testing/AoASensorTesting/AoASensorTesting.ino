#include <Arduino.h>
#include "MagEncoder.h"

MagEncoder magEncoder;

void setup() {
    Serial.begin(57600);
    magEncoder = MagEncoder(4, 7, 8);
}


void loop() {
    Serial.println(magEncoder.getRawData());
}