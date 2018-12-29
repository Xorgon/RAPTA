//
// Created by Elijah on 28/11/2018.
//

#include "ECU.h"

ECU::ECU() {}

ECU::ECU(uint8_t softSerialRX, uint8_t softSerialTX) {
    AltSoftSerial *softSerial = new AltSoftSerial(softSerialRX, softSerialTX);
    softSerial->begin(9600);
    ecuSerial = softSerial;
}

ECU::ECU(HardwareSerial &hardwareSerial) {
    ecuSerial = &hardwareSerial;
    hardwareSerial.begin(9600);
}

void ECU::updateData() {
    char cmd[] = "RCV";
    sendCommand(cmd);
    delay(50);  // TODO: Make a better system that doesn't rely on these delays.
    readCurrentValues();
}

void ECU::updateStatus() {
    status = getData("RSD");
}

void ECU::updateAll() {
    updateData();
    updateStatus();
}

bool ECU::checkCmdMatch(char *cmd, ecu_response_t resp) {
    return (resp.cmd[0] != cmd[0] or resp.cmd[1] != cmd[1] or resp.cmd[2] != cmd[2]);
}

String ECU::getData(char cmd[3]) {
    sendCommand(cmd);
    delay(50);
    ecu_response_t resp = readMessage();
    if (checkCmdMatch(cmd, resp)) {
        return "RECEIVED WRONG COMMAND";
    } else if (!resp.valid) {
        return "INVALID RESPONSE";
    } else {
        return String(resp.response);
    }
}

void ECU::sendCommand(char *cmd) {
    ecuSerial->write(SYNC);
    ecuSerial->write(SEPARATOR);
    ecuSerial->write(cmd);
    ecuSerial->write(SEPARATOR);
    ecuSerial->write(CR);
}

ecu_response_t ECU::readMessage() {
    ecu_response_t response;
    response.valid = false;

    // Read command return message
    bool synced = false;
    while (!synced and ecuSerial->available()) {
        char received = ecuSerial->read();
        if (received == SYNC) {
            synced = true;
            response.valid = true;
        }
    }
    if (ecuSerial->read() != SEPARATOR) { response.valid = false; }

    for (int i = 0; i < 3; i++) {
        response.cmd[i] = ecuSerial->read();
    }

    if (ecuSerial->read() != SEPARATOR) { response.valid = false; }
    if (ecuSerial->read() != CR) { response.valid = false; }

    // Read data message
    if (char(ecuSerial->read()) != SYNC) { response.valid = false; }
    if (ecuSerial->read() != SEPARATOR) { response.valid = false; }

    uint8_t charsRead = 0;
    char received = ecuSerial->read();
    while (received != CR and ecuSerial->available()) {
        response.response[charsRead] = received;
        charsRead++;
        received = ecuSerial->read();
    }
    response.response[charsRead] = '\0';
    return response;
}

void ECU::readCurrentValues() {
    ecu_response_t response;
    response.valid = false;

    // Read command return message
    bool synced = false;
    while (!synced and ecuSerial->available()) {
        char received = ecuSerial->read();
        if (received == SYNC) {
            synced = true;
            response.valid = true;
        }
    }
    if (ecuSerial->read() != SEPARATOR) { response.valid = false; }

    for (int i = 0; i < 3; i++) {
        response.cmd[i] = ecuSerial->read();
    }

    if (ecuSerial->read() != SEPARATOR) { response.valid = false; }
    if (ecuSerial->read() != CR) { response.valid = false; }

    // Read data message
    if (char(ecuSerial->read()) != SYNC) { response.valid = false; }
    if (ecuSerial->read() != SEPARATOR) { response.valid = false; }

    data.rpm = ecuSerial->parseInt();
    data.egt = ecuSerial->parseInt();
    data.pumpPower = ecuSerial->parseFloat();
    data.batVoltage = ecuSerial->parseFloat();
    data.throttlePct = ecuSerial->parseInt();
}