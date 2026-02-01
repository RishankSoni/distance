// SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
// SPDX-License-Identifier: MPL-2.0

#include <Arduino_RouterBridge.h>
#include <Arduino_Modulino.h>

// 1. Change Object to Distance
ModulinoDistance distanceSensor;

unsigned long previousMillis = 0;
// Distance sensors don't need to be read as fast as accelerometers. 
// 100ms (10Hz) is a good speed.
const long interval = 100; 

void setup() {
  Bridge.begin();

  // Initialize Modulino I2C communication (usually Wire1 on these boards)
  Modulino.begin(Wire1);

  // 2. Detect and connect to Distance sensor
  while (!distanceSensor.begin()) {
    // Retry every second if sensor not found
    delay(1000);
  }
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // 3. Read the sensor
    if (distanceSensor.available()) {
      int measurement_mm = distanceSensor.get();
      
      // Filter out invalid readings (sometimes returns -1 if out of range)
      if (measurement_mm >= 0) {
        // 4. Send "update_distance" with 1 argument (the integer)
        Bridge.notify("update_distance", measurement_mm);      
      }
    }
  }
}