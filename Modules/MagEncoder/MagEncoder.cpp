//
// TODO: Zero the value on initialization and read as degrees from zero (+/-).
//

#include "MagEncoder.h"

MagEncoder::MagEncoder() {}

MagEncoder::MagEncoder(uint8_t chipSelect, uint8_t clock, uint8_t data) {
    this->chipSelect = chipSelect;
    this->clock = clock;
    this->data = data;

    pinMode(chipSelect, OUTPUT);
    pinMode(clock, OUTPUT);
    pinMode(data, INPUT);

    digitalWrite(clock, HIGH);
    digitalWrite(chipSelect, HIGH);
}

unsigned int MagEncoder::getRawData() {
    unsigned int dataOut = 0;

    digitalWrite(chipSelect, LOW);
    delayMicroseconds(1); //Waiting for Tclkfe

    //Passing 10 times, from 0 to 9
    for (int x = 0; x < 10; x++) {
        digitalWrite(clock, LOW);
        delayMicroseconds(1); //Tclk/2
        digitalWrite(clock, HIGH);
        delayMicroseconds(1); //Tdo valid, like Tclk/2

        //shift all the entering data to the left and past the pin state to it. 1e bit is MSB
        dataOut = (dataOut << 1) | digitalRead(data);
    }

    digitalWrite(chipSelect, HIGH);
    return dataOut;
}