/*
 * Based on code by Juan Pedro López
 * https://discuss.ardupilot.org/t/mavlink-and-arduino-step-by-step/25566
 */

#ifndef RAPTA_PXCOMMS_H
#define RAPTA_PXCOMMS_H

#include <Arduino.h>
#include <mavlink.h>
#include <AltSoftSerial.h>

class PXComms {
public:
    PXComms();

    PXComms(HardwareSerial &hardwareSerial);

    PXComms(uint8_t soft_serial_rx, uint8_t soft_serial_tx);

    void send_heartbeat();

    void send_data_request();

    void receive_data();

    float get_airspeed();

private:
    mavlink_vfr_hud_t vfr_hud_data;
    mavlink_sys_status_t sys_status;
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    Stream *px_serial;
};


#endif //RAPTA_PXCOMMS_H
