#include <Arduino.h>
#include <Servo.h>

Servo out;

void setup() {
    out.attach(10);
    out.writeMicroseconds(1000);
}

void loop() {

}
