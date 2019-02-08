//
// Created by Elijah on 28/11/2018.
//

#include "ECU.h"

ECU::ECU() {}

ECU::ECU(HardwareSerial &hardwareSerial) {
    ecuSerial = &hardwareSerial;
    hardwareSerial.begin(9600);
    last_cmd_millis = 0;
    last_cmd = "RSD";
}

void ECU::updateData() {
    char cmd[] = "RCV";
    sendCommand(cmd);
    delay(50);
    ecu_response_t resp;
    readHeader(&resp);
    readCurrentValues(&resp);
}

void ECU::updateStatus() {
    status = getData("RSD");
}

void ECU::updateAll() {
    unsigned long now = millis();
    if (now - last_cmd_millis > CMD_DELAY) {
        if (ecuSerial->available()) {
            ecu_response_t resp;
            receiveResponse(&resp);
        }
        if (strcmp(last_cmd, "RSD") == 0) {
            sendCommand("RCV");
            last_cmd = "RCV";
        } else {
            sendCommand("RSD");
            last_cmd = "RSD";
        }
        last_cmd_millis = now;
    }
}

String ECU::getData(char cmd[3]) {
    sendCommand(cmd);
    delay(50);
    ecu_response_t resp;
    readHeader(&resp);
    readMessage(&resp);
    if (strcmp(resp.cmd, cmd)) {
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

void ECU::readHeader(ecu_response_t *response) {
    response->valid = false;

    // Read command return message
    bool synced = false;
    while (!synced and ecuSerial->available()) {
        char received = ecuSerial->read();
        if (received == SYNC) {
            synced = true;
            response->valid = true;
        }
    }
    if (ecuSerial->read() != SEPARATOR) { response->valid = false; }

    for (int i = 0; i < 3; i++) {
        response->cmd[i] = ecuSerial->read();
    }
    response->cmd[3] = '\0';

    if (ecuSerial->read() != SEPARATOR) { response->valid = false; }
    if (ecuSerial->read() != CR) { response->valid = false; }
}

void ECU::readMessage(ecu_response_t *response) {
    // Read data message
    if (char(ecuSerial->read()) != SYNC) { response->valid = false; }
    if (ecuSerial->read() != SEPARATOR) { response->valid = false; }

    uint8_t charsRead = 0;
    char received = ecuSerial->read();
    while (received != CR and ecuSerial->available()) {
        response->response[charsRead] = received;
        charsRead++;
        received = ecuSerial->read();
    }
    response->response[charsRead] = '\0';
    return response;
}

void ECU::readCurrentValues(ecu_response_t *response) {
    // Read data message
    if (char(ecuSerial->read()) != SYNC) { response->valid = false; }
    if (ecuSerial->read() != SEPARATOR) { response->valid = false; }

    data.rpm = ecuSerial->parseInt();
    data.egt = ecuSerial->parseInt();
    data.pumpPower = ecuSerial->parseFloat();
    data.batVoltage = ecuSerial->parseFloat();
    data.throttlePct = ecuSerial->parseInt();
}

void ECU::receiveResponse(ecu_response_t *response) {
    readHeader(response);
    if (!response->valid) {
        return;
    }

    if (strcmp(response->cmd, "RCV") == 0) {
        readCurrentValues(response);
    } else if (strcmp(response->cmd, "RSD") == 0) {
        readMessage(response);
        status = String(response->response);
    } else {
        readMessage(response);
    }
}