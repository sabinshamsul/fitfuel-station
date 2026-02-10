# 🚀 FitFuel Vending Machine - Deployment Guide

This document outlines the steps to deploy, configure, and maintain the FitFuel Vending Machine software on a production kiosk or vending unit.

## 1. System Requirements
*   **OS:** Windows 10/11 (Recommended for driver support) or Linux (Ubuntu 20.04+).
*   **Python:** Version 3.9 or higher.
*   **Hardware:**
    *   Touchscreen Display (1920x1080 recommended).
    *   Internet connection (required for OpenAI fallback features).
    *   OMRON Body Composition Monitor (or compatible scale).

## 2. Installation

1.  **Install Python Dependencies:**
    Open a terminal/command prompt in the project folder and run:
    ```bash
    pip install Pillow openai
    ```
    *   `Pillow`: Handles image processing for the UI.
    *   `openai`: Handles the AI fallback logic for recipe generation.

2.  **Verify Assets:**
    Ensure a folder named `assets` exists in the same directory as `main.py` and contains:
    *   `gym_bg_1.jpg`
    *   `gym_bg_2.jpg`
    *   `gym_bg_3.jpg`

## 3. Configuration

### A. OpenAI API Key (Crucial for AI Features)
Do not hardcode the key in the file. Set it as a system environment variable on the vending machine PC.

**Windows:**
1.  Search for **"Edit the system environment variables"**.
2.  Click **"Environment Variables"**.
3.  Under **System variables**, click **New**.
4.  **Variable name:** `OPENAI_API_KEY`
5.  **Variable value:** `sk-your-actual-api-key-here`

### B. Screen Resolution
The system attempts to auto-detect fullscreen resolution. If you need to force a specific size, edit `config.py`:
```python
WIDTH = 1920  # Set manually if auto-detect fails
HEIGHT = 1080
```

## 4. Hardware Integration (Sensor Data)
The software reads body composition data from `sensor_data.csv`.

*   **Integration Point:** You must configure your scale/sensor driver software to write the latest scan results to this CSV file immediately after a user completes a scan.
*   **File Location:** Same directory as `main.py`.
*   **Required Format:**
    ```csv
    body_weight_kg,skeletal_muscle_percent,resting_metabolic_rate,body_fat_percent,timestamp
    75.5,35.2,1650,22.3,2025-01-14 10:00:00
    ```

## 5. Running the Application
To start the kiosk software:
```bash
python main.py
```
*   The app will launch in **Fullscreen Mode**.
*   To exit fullscreen during testing, press **ESC**.

## 6. Maintenance & Troubleshooting

### Accessing Maintenance Mode
If the machine needs service (e.g., checking logs, closing the app) without a keyboard:
1.  Tap the **Gear Icon (⚙️)** in the top-left corner of the landing screen.
2.  Enter the PIN: **1234**.

### Periodic Maintenance (Cache & Logs)
*   **Clear Logs:** Every 1-3 months, use the Maintenance Menu ("Clear Logs" button) to reset `fitfuel_station.log`.
*   **Python Cache:** If you update the software code, delete the `__pycache__` folder before restarting to ensure the new code loads cleanly.

### Common Issues
*   **"OpenAI module not found":** Run `pip install openai`.
*   **"Sensor data file not found":** Ensure the scale driver is creating `sensor_data.csv`. The app will generate a sample one for testing if missing.
*   **UI Freezing:** The app has an inactivity timer (30s) that resets to the start screen. Ensure the touchscreen is registering inputs correctly.

---
*FitFuel Vending System v2.0*