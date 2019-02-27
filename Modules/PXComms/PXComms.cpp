//
// TODO: Clean up id parameters (sys_id, comp_id etc.)
//

#include "PXComms.h"


PXComms::PXComms() {}

PXComms::PXComms(HardwareSerial &hardware_serial) {
    px_serial = &hardware_serial;
    hardware_serial.begin(115200);
    initialize_counters();
}

void PXComms::initialize_counters() {
    previousMillisMAVLink = 0;     // will store last time MAVLink was transmitted and listened
    next_interval_MAVLink = 1000;  // next interval to count
    num_hbs = 60;                      // # of heartbeats to wait before activating STREAMS from Pixhawk. 60 = one minute.
    num_hbs_sent = num_hbs;
}

void PXComms::send_heartbeat() {
    uint8_t sys_id = 1;
    uint8_t comp_id = 0;

    uint8_t system_type = MAV_TYPE_FIXED_WING;
    uint8_t autopilot_type = MAV_AUTOPILOT_INVALID;

    uint8_t system_mode = MAV_MODE_PREFLIGHT; ///< Booting up
    uint32_t custom_mode = 0;                 ///< Custom mode, can be defined by user/adopter
    uint8_t system_state = MAV_STATE_STANDBY; ///< System ready for flight

    mavlink_msg_heartbeat_pack(sys_id, comp_id, &(msg), system_type, autopilot_type, system_mode, custom_mode,
                               system_state);

    // Copy the message to the send buffer
    uint16_t len = mavlink_msg_to_send_buffer(buf, &(msg));

    px_serial->write(buf, len);
}

void PXComms::send_data_request() {
// To be setup according to the needed information to be requested from the Pixhawk
    const int maxStreams = 1;
    const uint8_t MAVStreams[maxStreams] = {MAV_DATA_STREAM_EXTENDED_STATUS};
    const uint16_t MAVRates[maxStreams] = {0x02};

    for (int i = 0; i < maxStreams; i++) {
        /*
         * mavlink_msg_request_data_stream_pack(system_id, component_id,
         *    &msg,
         *    target_system, target_component,
         *    MAV_DATA_STREAM_POSITION, 10000000, 1);
         *
         * mavlink_msg_request_data_stream_pack(uint8_t system_id, uint8_t component_id,
         *    mavlink_message_t* msg,
         *    uint8_t target_system, uint8_t target_component, uint8_t req_stream_id,
         *    uint16_t req_message_rate, uint8_t start_stop)
         *
         */
        mavlink_msg_request_data_stream_pack(2, 200, &msg, 1, 0, MAVStreams[i], MAVRates[i], 1);
        uint16_t len = mavlink_msg_to_send_buffer(buf, &(msg));
        px_serial->write(buf, len);
    }
}

void PXComms::receive_data() {

    mavlink_message_t msg;
    mavlink_status_t status;


    while (px_serial->available() > 0) {
        uint8_t c = px_serial->read();
        // Try to get a new message
        if (mavlink_parse_char(MAVLINK_COMM_0, c, &msg, &status)) {
            // Handle message
            switch (msg.msgid) {
                case MAVLINK_MSG_ID_HEARTBEAT:  // #0: Heartbeat
                {
                    // E.g. read GCS heartbeat and go into
                    // comm lost mode if timer times out
                }
                    break;

                case MAVLINK_MSG_ID_SYS_STATUS:  // #1: SYS_STATUS
                {
                    /* Message decoding: PRIMITIVE
                     *    mavlink_msg_sys_status_decode(const mavlink_message_t* msg, mavlink_sys_status_t* sys_status)
                     */
                    //mavlink_message_t* msg;
                    mavlink_msg_sys_status_decode(&msg, &(sys_status));
                }
                    break;

                case MAVLINK_MSG_ID_PARAM_VALUE:  // #22: PARAM_VALUE
                {
                    /* Message decoding: PRIMITIVE
                     *    mavlink_msg_param_value_decode(const mavlink_message_t* msg, mavlink_param_value_t* param_value)
                     */
                    mavlink_param_value_t param_value;
                    mavlink_msg_param_value_decode(&msg, &param_value);
                }
                    break;

                case MAVLINK_MSG_ID_RAW_IMU:  // #27: RAW_IMU
                {
                    /* Message decoding: PRIMITIVE
                     *    static inline void mavlink_msg_raw_imu_decode(const mavlink_message_t* msg, mavlink_raw_imu_t* raw_imu)
                     */
                    mavlink_raw_imu_t raw_imu;
                    mavlink_msg_raw_imu_decode(&msg, &raw_imu);
                }
                    break;

                case MAVLINK_MSG_ID_ATTITUDE:  // #30
                {
                    /* Message decoding: PRIMITIVE
                     *    mavlink_msg_attitude_decode(const mavlink_message_t* msg, mavlink_attitude_t* attitude)
                     */
                    mavlink_attitude_t attitude;
                    mavlink_msg_attitude_decode(&msg, &attitude);
                }
                    break;

                case MAVLINK_MSG_ID_VFR_HUD: // #74
                {
                    mavlink_msg_vfr_hud_decode(&msg, &(vfr_hud_data));
                }

                case MAVLINK_MSG_ID_GPS_STATUS:
                {
                    mavlink_msg_gps_status_decode(&msg, &(gps_status));
                }

                default:
                    break;
            }
        }
    }
}

void PXComms::update_data() {
    unsigned long currentMillisMAVLink = millis();
    if (currentMillisMAVLink - previousMillisMAVLink >= next_interval_MAVLink) {
        previousMillisMAVLink = currentMillisMAVLink;
        send_heartbeat();
        num_hbs_sent++;
        if (num_hbs_sent >= num_hbs) {
            // Request streams from Pixhawk
            send_data_request();
            num_hbs_sent = 0;
        }
    }
    receive_data();
}

float PXComms::get_airspeed() {
    return this->vfr_hud_data.airspeed;
}

float PXComms::get_altitude() {
    return this->vfr_hud_data.alt;
}

int8_t PXComms::get_battery_pcnt() {
    return this->sys_status.battery_remaining;
}

uint16_t PXComms::get_battery_mv() {
    return this->sys_status.voltage_battery;
}

uint8_t PXComms::get_gps_sats() {
    return this->gps_status.satellites_visible;
}