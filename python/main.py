# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import App, Logger, Bridge
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from datetime import datetime, UTC
import requests
import time

# --- CONFIGURATION ---
SERVER_URL = "http://10.13.162.30:5000/speak"
TRIGGER_OBJECT = "person" 
ALERT_COOLDOWN = 5.0      
last_alert_time = 0

# Store the latest distance reading here (default to -1 means "no data yet")
current_distance = -1 

logger = Logger("smart-vision-system")
ui = WebUI()

# Initialize Object Detection (built-in YOLOX-Nano)
detection_stream = VideoObjectDetection(confidence=0.5, debounce_sec=0.0)

# --- 1. TTS FUNCTION ---
def speak_text(text):
    payload = {"text": text}
    try:
        # Short timeout to prevent lag
        response = requests.post(SERVER_URL, json=payload, timeout=5)
        if response.status_code == 200:
            logger.info(f"✅ TTS Success: {text}")
        else:
            logger.warning(f"⚠️ TTS Server Error {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Could not reach TTS server at {SERVER_URL}")

# --- 2. DISTANCE SENSOR HANDLER ---
# This function runs whenever the C++ sketch sends "update_distance"
def update_distance(mm: int):
    global current_distance
    current_distance = mm
    
  

# --- 3. VIDEO DETECTION HANDLER ---
def handle_detections(detections: dict):
    global last_alert_time, current_distance
    current_time = time.time()

    for key, value in detections.items():
        # Update Web Dashboard
        entry = {
            "content": key,
            "confidence": value.get("confidence"),
            "timestamp": datetime.now(UTC).isoformat()
        }
        ui.send_message("detection", message=entry)

        # TTS TRIGGER LOGIC
        if value.get("confidence") > 0.6:
            if (current_time - last_alert_time) > ALERT_COOLDOWN:
                
                # Construct the message based on sensor data
                if current_distance > 0 and current_distance < 2000:
                    # If we have valid distance data
                    message = f"I see a {key} at {current_distance/10} centimeters"
                else:
                    # If sensor is blocked or out of range
                    message = f"I see a {key}"

                logger.info(f"Triggering Voice: {message}")
                speak_text(message)
                last_alert_time = current_time

# --- SETUP ---

# Link UI threshold slider
ui.on_message("override_th", lambda sid, threshold: detection_stream.override_threshold(threshold))

# Connect the Video Stream callback
detection_stream.on_detect_all(handle_detections)

# Connect the Distance Sensor callback (Bridge)
Bridge.provide("update_distance", update_distance)

print(f"--- System Started: Looking for {TRIGGER_OBJECT} & Reading Distance ---")
App.run()