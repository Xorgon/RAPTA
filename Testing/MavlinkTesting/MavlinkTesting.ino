#include "mavlink.h"
#include "PXComms.h"

// Mavlink variables
unsigned long previousMillisMAVLink = 0;     // will store last time MAVLink was transmitted and listened
unsigned long next_interval_MAVLink = 1000;  // next interval to count
const int num_hbs = 60;                      // # of heartbeats to wait before activating STREAMS from Pixhawk. 60 = one minute.
int num_hbs_sent = num_hbs;
PXComms px_comms;

void setup() {
    px_comms = PXComms(Serial1);
    Serial.begin(57600);
    Serial.println("MAVLink starting.");
}

void loop() {
    unsigned long currentMillisMAVLink = millis();

    if (currentMillisMAVLink - previousMillisMAVLink >= next_interval_MAVLink) {
        previousMillisMAVLink = currentMillisMAVLink;
        px_comms.send_heartbeat();
        num_hbs_sent++;
        if (num_hbs_sent >= num_hbs) {
            // Request streams from Pixhawk
            px_comms.send_data_request();
            num_hbs_sent = 0;
        }

    }

    px_comms.receive_data();
    Serial.println(px_comms.get_airspeed());
}