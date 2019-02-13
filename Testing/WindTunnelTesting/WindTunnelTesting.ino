#include <Arduino.h>
#include "Servo.h"
#include "MagEncoder.h"
#include "PXComms.h"

MagEncoder aoaSensor;
PXComms pixhawk;

char output[500];

uint8_t configChangePin = 2;
uint16_t lowerThreshold = 1450; // If lower than this, move down a configuration
uint16_t upperThreshold = 1550; // If higher than this, move up a configuration
bool changed = false;
uint8_t config = 0;
uint8_t max_config = 1;
uint32_t lastPWMTime;
uint16_t pwmValue;

String aileronConfigLabels[] = {"5"};
uint16_t aileronConfigs[] = {1500};
uint8_t aileronServoPin = 30;
Servo aileronServo;

String portTailConfigLabels[] = {"5"};
uint16_t portTailConfigs[] = {1500};
uint8_t portTailServoPin = 31;
Servo portTailServo;

String stbdTailConfigLabels[] = {"5"};
uint16_t stbdTailConfigs[] = {1500};
uint8_t stbdTailServoPin = 32;
Servo stbdTailServo;

String flapConfigLabels[] = {"5"};
uint16_t flapConfigs[] = {1500};
uint8_t flapServoPin = 33;
Servo flapServo;

void setup() {
    Serial.begin(57600);

    aileronServo.attach(aileronServoPin);
    portTailServo.attach(portTailServoPin);
    stbdTailServo.attach(stbdTailServoPin);
    flapServo.attach(flapServoPin);

    updateOutput();

    pixhawk = PXComms(Serial2);
    aoaSensor = MagEncoder(4, 7, 8);
    pixhawk.send_data_request();
    attachInterrupt(digitalPinToInterrupt(configChangePin), onRising, RISING);
}

void loop() {
    if (!changed) {
        if (pwmValue > upperThreshold && config < max_config) {
            config++;
            changed = true;
        } else if (pwmValue < lowerThreshold && config > 0) {
            config--;
            changed = true;
        }
    } else {
        if (pwmValue > lowerThreshold && pwmValue < upperThreshold) {
            changed = false;
        }
    }
    updateOutput();

    float angle = aoaSensor.getAngle();
    pixhawk.receive_data();

    sprintf(output, "%lu,%s,%s,%i,%i,%s,%s,%s,%s~",
            millis(),
            String(pixhawk.get_airspeed()).c_str(),
            String(angle).c_str(),
            pixhawk.get_battery_pcnt(),
            config,
            aileronConfigLabels[config].c_str(),
            portTailConfigLabels[config].c_str(),
            stbdTailConfigLabels[config].c_str(),
            flapConfigLabels[config].c_str()
    );
    Serial.println(output);
    delay(50);
}


void onRising() {
    attachInterrupt(digitalPinToInterrupt(configChangePin), onFalling, FALLING);
    lastPWMTime = micros();
}

void onFalling() {
    attachInterrupt(digitalPinToInterrupt(configChangePin), onRising, RISING);
    pwmValue = micros() - lastPWMTime;
}

void updateOutput() {
    aileronServo.writeMicroseconds(aileronConfigs[config]);
    portTailServo.writeMicroseconds(portTailConfigs[config]);
    stbdTailServo.writeMicroseconds(stbdTailConfigs[config]);
    flapServo.writeMicroseconds(flapConfigs[config]);
}
