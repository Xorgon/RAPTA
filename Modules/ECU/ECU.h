//
// Created by Elijah on 28/11/2018.
//

#ifndef RAPTA_ECU_H
#define RAPTA_ECU_H

#define SYNC char(0xC7)
#define SEPARATOR char(0x2C)
#define CR char(0x0D)
#define MAX_RESPONSE_LENGTH 100

#include <AltSoftSerial.h>

typedef struct __ecu_response_t {
    bool valid;
    char cmd[3];
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

    ECU(uint8_t softSerialRX, uint8_t softSerialTX);

    ECU(HardwareSerial &hardwareSerial);

    String ECU::getData(char cmd[3]);

    void sendCommand(char *cmd);

    void updateData();

    void updateStatus();

    void updateAll();

    ecu_response_t readMessage();

    eng_data_t data;

    String status;
private:

    bool checkCmdMatch(char cmd[3], ecu_response_t resp);

    void readCurrentValues();

    Stream *ecuSerial;
};

#endif //RAPTA_ECU_H
