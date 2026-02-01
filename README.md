# Smart Blind Stick with AI Object Detection

An advanced assistive device built on the **Arduino UNO Q** that provides *“auditory sight”* to individuals with visual impairments. This project combines local edge AI for person detection with millimetric distance sensing to offer real-time verbal navigation cues.

---

## 🚀 Project Overview

The Smart Blind Stick continuously monitors the user's path using a USB camera and the built-in **YOLOX-Nano** object detection model. When a person is detected, the system calculates their exact distance using a Time-of-Flight sensor and triggers a Text-to-Speech (TTS) engine to announce the obstacle (e.g., *“I see a person at 1200 millimeters”*).

### Key Features
- **Edge AI Processing**: Runs entirely on the Arduino UNO Q (Qualcomm Dragonwing™️ MPU), ensuring complete privacy and zero latency.
- **Dual-Brain Architecture**: Separates high-level AI intelligence from real-time sensor management for maximum reliability.
- **Millimetric Accuracy**: Uses the Modulino Distance sensor for precise depth perception.
- **Voice Feedback**: Provides natural language alerts through an external TTS server.

---

## 🛠 Hardware Lineup

- **Core Controller**: [Arduino UNO Q](https://store.arduino.cc/uno-q) (Qualcomm Dragonwing™️ MPU + STM32U585 MCU)
- **Vision Input**: Standard USB Webcam (connected via USB-C)
- **Distance Sensor**: **Modulino Distance** sensor (Time-of-Flight), connected via the I2C/QWIIC interface
- **Audio Output**: External speaker connected to a host running the TTS Flask server
- **Connectivity**: Integrated Wi-Fi®️ for communicating with the audio server

---

## 📂 Repository Structure

- `python/` — Contains `main.py`, the logic hub running on the MPU (Linux)
- `sketch/` — Contains `sketch.ino`, the real-time sensor polling code running on the MCU
- `app.yaml` — Application configuration for the Arduino App Lab
- `tts.py` - Code for convert text to speech
- `.gitignore` — Standard exclusions for project builds

---

## ⚙️ Software Architecture

This project leverages the **Arduino App Lab** and the board’s specialized processors:

1. **MPU (Linux Intelligence)**  
   Processes the video stream using the **Video Object Detection Brick (YOLOX-Nano)**. It coordinates the logic of when a detection is confident enough to trigger a voice alert.

2. **MCU (Real-Time Control)**  
   Dedicated to the **Modulino Distance** sensor. It polls raw distance data every 100 ms and sends it to the processor via the **RPC Bridge**.

3. **TTS Server**  
   A lightweight Python Flask server that receives text strings via HTTP and synthesizes them into speech using `pyttsx3`.

---

## 💻 Installation & Setup

### 1. Arduino App Lab
1. Connect your **Arduino UNO Q** to your PC and open the **Arduino App Lab**.
2. Create a new application and import the files from this repository.
3. Ensure the **Video Object Detection** and **WebUI** Bricks are added to your project.

### 2. TTS Server Setup
1. On a host machine, run the Flask server:
   ```bash
   python3 tts.py
