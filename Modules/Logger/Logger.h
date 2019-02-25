//
// Created by Elijah on 14/02/2017.
//

#ifndef RAPTA_LOGGER_H
#define RAPTA_LOGGER_H

#include <Arduino.h>
#include <SD.h>

/**
 * Allows for easy logging of information to the SD card and to the Serial monitor using log().
 *
 * The Logger writes "FLIGHTX.LOG" files to the logs folder on the SD card.
 *
 * The flights are numerically ordered, so the first flight would be FLIGHT1.LOG.
 *
 * \see Logger::log() for logging data.
 *
 * @author Elijah Andrews
 */
class Logger {
public:
    Logger(int sdChipSelect);

    Logger();

    void log(String tag, String data);

    void log(String logLine);

    void checkFlush(uint16_t logLineLength);

    void checkFlush();

    String parseMillis(uint32_t millis);

private:

    File logFile;

    uint16_t bytesWritten;

    uint32_t lastFlushed;

    String getNextName();

};

#endif //RAPTA_LOGGER_H
