//
// Created by Elijah on 28/11/2018.
//

#ifndef RAPTA_ECU_H
#define RAPTA_ECU_H

#include <Arduino.h>

#define SYNC char(0xC7)
#define SEPARATOR char(0x2C)
#define CR char(0x0D)
#define MAX_RESPONSE_LENGTH 100

#define CMD_DELAY 50

typedef struct __ecu_response_t {
    bool valid;
    char cmd[4];
    char response[MAX_RESPONSE_LENGTH];
} ecu_response_t;

typedef struct __eng_data_t {
    uint32_t rpm;
    uint16_t egt;
    float pumpPower;
    float batVoltage;
    uint8_t throttlePct;
} eng_data_t;

class ECU {
public:
    ECU();

    ECU(HardwareSerial &hardwareSerial);

    String ECU::getData(char cmd[3]);

    void sendCommand(char *cmd);

    /**
     * Updates engine data. Relies on delays so use for testing only.
     */
    void updateData();

    /**
     * Updates engine data and status. Use this for most applications.
     */
    void updateAll();

    void receiveResponse(ecu_response_t *response);

    eng_data_t data;

    char status[33];

private:
    Stream *ecuSerial;
    unsigned long last_cmd_millis;
    char *last_cmd;

    void readHeader(ecu_response_t *response);

    void readCurrentValues(ecu_response_t *response);

    void readMessage(ecu_response_t *response);
};

#endif //RAPTA_ECU_H
