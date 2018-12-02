//
// Created by Elijah on 28/11/2018.
//

#ifndef RAPTA_ECU_H
#define RAPTA_ECU_H

#define SYNC 0xC7
#define SEPARATOR 0x2C
#define CR 0x0D
#define MAX_RESPONSE_LENGTH 100

#include <AltSoftSerial.h>

class ECU {
public:
    ECU();

    ECU(uint8_t softSerialRX, uint8_t softSerialTX);

    ECU(HardwareSerial &hardwareSerial);

	void sendCommand(char *cmd);
	
    String readCurrentValues();

	String readResponse(HardwareSerial &debugSerial);
	
private:
    Stream *ecuSerial;

    String readResponse();
};

#endif //RAPTA_ECU_H
