# 🍌 Fruit Ripeness Detection using Machine Learning

## 📌 Overview

This project predicts fruit ripeness using gas sensors (MQ135), environmental data (temperature, pressure), and machine learning.

## 🚀 Features

* Real-time sensor data collection
* Automatic baseline calibration
* Delta-based gas analysis
* Machine Learning prediction (Random Forest)
* Outputs: Days to ripeness + Stage (Unripe / Ripening / Ripe)

## 🧠 Tech Stack

* Python
* ESP32 (Arduino)
* MQ135 Gas Sensor
* BME280 Sensor
* Scikit-learn

## 📊 Model Performance

* MAE: 0.10
* R² Score: 0.98

## ⚙️ How to Run

```bash
python logger.py
python prepare_dataset.py
python train_model.py
```

## 📸 Results

(Add your graphs here)

## 🔮 Future Scope

* IoT integration
* Mobile app support
* Advanced ML models
