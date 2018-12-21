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

String ECU::readCurrentValues() {
    sendCommand("RCV");
    return readResponse();
}

void ECU::sendCommand(char *cmd) {
    ecuSerial->write(SYNC);
    ecuSerial->write(SEPARATOR);
    ecuSerial->write(cmd);
    ecuSerial->write(SEPARATOR);
    ecuSerial->write(CR);
}

String ECU::readResponse() {
    char response[MAX_RESPONSE_LENGTH];
    uint16_t response_char_count = 0;
    bool synced = false;

    if (!ecuSerial->available()) {
        return F("Serial not available.");
    }

    while (!synced) {
        if (ecuSerial->read() == SYNC) {
            synced = true;
        }
    }

    if (ecuSerial->read() != SEPARATOR) {
        return F("Response missing separator.");
    }

    while (ecuSerial->available()) {
        byte c = ecuSerial->read();
        if (c != SEPARATOR) {
            response[response_char_count] = (char) c;
            response_char_count++;
        } else {
            break;
        }
    }

    if (ecuSerial->read() != CR) {
        return F("Did not receive CR.");
    }

    return String(response);
}

String ECU::readResponse(HardwareSerial &debugSerial) {
    char response[MAX_RESPONSE_LENGTH];
    uint16_t response_char_count = 0;
    bool synced = false;

    while (!ecuSerial->available()) {
        debugSerial.println("ecuSerial is not yet available...");
    }

    while (!synced) {
        char received = ecuSerial->read();
        debugSerial.println("Awaiting sync byte (got '" + String(uint8_t(received)) + "')");
        if (received == SYNC) {
            synced = true;
            debugSerial.println("Received sync byte...");
        }
    }

    if (ecuSerial->read() != SEPARATOR) {
        return F("Response missing separator.");
    }

    while (ecuSerial->available()) {
        debugSerial.println("Receiving...");
        byte c = ecuSerial->read();
        if (c != SEPARATOR) {
            response[response_char_count] = (char) c;
            response_char_count++;
        } else {
            break;
        }
    }

    if (ecuSerial->read() != CR) {
        return F("Did not receive CR.");
    }

    return String(response);
}