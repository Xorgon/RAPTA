#include <Arduino.h>
#include "Servo.h"
#include "ECU.h"
#include "MagEncoder.h"
#include "PXComms.h"
#include "HX711.h"
#include "Logger.h"
#include <stdlib.h>
#include <math.h>

#define rssiPin A0
#define LOAD_CELL_DOUT  13
#define LOAD_CELL_CLK  12
#define LOAD_CELL_QUOTIENT 219371.22
#define TELEM_INTERVAL 1000
#define FUEL_SENSOR 35

typedef union {
    struct {
        uint32_t time;
        float ias;
        float alt;
        eng_data_t eng_data;
        float aoa;
        char eng_status[32];
        float rssi;
        uint16_t batMilliVolts;
        float loadCellReading;
        int8_t fuel_pct; // 74
    } data;
    char s[sizeof(data)];
} telem_t;

ECU ecu;
MagEncoder aoaSensor;
PXComms pixhawk;
HX711 loadCell;
long loadCellReading;
long loadCellTare;
Logger logger;

telem_t telem_data;

ecu_response_t resp;
char output[500];

long last_sent_time;

void setup() {
    Serial.begin(57600);
    ecu = ECU(Serial1);
    pixhawk = PXComms(Serial2);
    aoaSensor = MagEncoder(4, 7, 8);
    loadCell = HX711(LOAD_CELL_DOUT, LOAD_CELL_CLK);
    while (!loadCell.is_ready()) {
        Serial.println(F("Waiting for load cell..."));
    }
    loadCellTare = loadCell.read();
    loadCellReading = 0;
    logger = Logger(5);
    pixhawk.send_data_request();
    last_sent_time = millis();
    pinMode(FUEL_SENSOR, INPUT); // Fuel sensor
}

void loop() {

    // Update data
    ecu.updateAll();
    pixhawk.receive_data();
    if (loadCell.is_ready()) {
        loadCellReading = loadCell.read() - loadCellTare;
    }
    int8_t fuel_pct;
    if (digitalRead(FUEL_SENSOR)) {
        fuel_pct = -1;
    } else {
        fuel_pct = 1;
    }

    // Store new data in telem_data
    updateData(&telem_data,
               millis(),
               pixhawk.get_airspeed(),
               pixhawk.get_altitude(),
               ecu.data,
               aoaSensor.getAngle(),
               ecu.status.c_str(),
               100 * (analogRead(rssiPin) * 4.8 / 3.3) / 1024,  // RSSI
               pixhawk.get_battery_mv(),
               loadCellReading,
               fuel_pct);

    // Log to file
    printDataToString(output, telem_data);
    logger.log(output);

    // Send over telemetry
    if (millis() - last_sent_time > TELEM_INTERVAL) {
        Serial.write('\xC7\xC7\xC7');
        Serial.write(telem_data.s, sizeof(telem_t));
        last_sent_time = millis();
    }
}

void updateData(telem_t *t, uint32_t time, float ias, float alt, eng_data_t eng_data, float aoa,
                char eng_status[32], float rssi, uint16_t batMilliVolts, float loadCellReading, int8_t fuel_pct) {
    (*t).data.time = time;
    (*t).data.ias = ias;
    (*t).data.alt = alt;
    (*t).data.eng_data = eng_data;
    (*t).data.aoa = aoa;
    strcpy((*t).data.eng_status, eng_status);
    (*t).data.rssi = rssi;
    (*t).data.batMilliVolts = batMilliVolts;
    (*t).data.loadCellReading = loadCellReading;
    (*t).data.fuel_pct = fuel_pct;
}

void printDataToString(char *out, telem_t t) {
    sprintf(out, "%lu,%s,%s,%lu,%u,%s,%s,%u,%s,%s,%s,%u,%lu,%s,%i",
            t.data.time,
            String(t.data.ias).c_str(),
            String(t.data.alt).c_str(),
            t.data.eng_data.rpm,
            t.data.eng_data.egt,
            String(t.data.eng_data.pumpPower).c_str(),
            String(t.data.eng_data.batVoltage).c_str(),
            t.data.eng_data.throttlePct,
            String(t.data.aoa).c_str(),
            t.data.eng_status,
            String(t.data.rssi).c_str(),
            t.data.batMilliVolts,
            String(t.data.loadCellReading).c_str(),
            t.data.fuel_pct);
}