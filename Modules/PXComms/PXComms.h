/*
 * Based on code by Juan Pedro López
 * https://discuss.ardupilot.org/t/mavlink-and-arduino-step-by-step/25566
 */

#ifndef RAPTA_PXCOMMS_H
#define RAPTA_PXCOMMS_H

#include <Arduino.h>
#include <mavlink.h>

class PXComms {
public:
    PXComms();

    PXComms(HardwareSerial &hardwareSerial);

    void send_heartbeat();

    void send_data_request();

    void receive_data();

    void update_data();

    float get_airspeed();

    float get_altitude();

    int8_t get_battery_pcnt();

    uint16_t get_battery_mv();

private:
    void initialize_counters();

    mavlink_vfr_hud_t vfr_hud_data;
    mavlink_sys_status_t sys_status;
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    Stream *px_serial;

    unsigned long previousMillisMAVLink;     // will store last time MAVLink was transmitted and listened
    unsigned long next_interval_MAVLink;  // next interval to count
    int num_hbs;                      // # of heartbeats to wait before activating STREAMS from Pixhawk. 60 = one minute.
    int num_hbs_sent;
};


#endif //RAPTA_PXCOMMS_H
