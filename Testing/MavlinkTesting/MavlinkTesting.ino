#include "mavlink.h"
#include "PXComms.h"

// Mavlink variables
PXComms px_comms;

char output[500];

void setup() {
    px_comms = PXComms(Serial2);
    Serial.begin(9600);
    Serial.println("MAVLink starting.");
    px_comms.send_data_request();
}

void loop() {
    px_comms.update_data();
    sprintf(output, "%s, %s",
            String(px_comms.get_airspeed()).c_str(),
            String(px_comms.get_altitude()).c_str()
    );
    Serial.println(output);
}

void serialEvent2() {

}