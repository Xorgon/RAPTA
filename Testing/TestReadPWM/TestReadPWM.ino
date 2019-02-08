#include <Arduino.h>
#include "Servo.h"

Servo pwmOut;
uint32_t lastPWMTime;
uint16_t pwmValue;

void setup() {
    Serial.begin(57600);
    attachInterrupt(digitalPinToInterrupt(2), onFalling, FALLING);
    pwmOut.attach(4);
    pwmOut.writeMicroseconds(1900);
}

void loop() {
    Serial.println(pwmValue);
}

void onRising() {
    attachInterrupt(digitalPinToInterrupt(2), onFalling, FALLING);
    lastPWMTime = micros();
}

void onFalling() {
    pwmValue = micros() - lastPWMTime;
    attachInterrupt(digitalPinToInterrupt(2), onRising, RISING);
}