# FreshScan — IoT-Based Fruit Quality Assessment

FreshScan is an academic prototype that explores fruit-ripeness assessment using gas and environmental sensor readings combined with a machine-learning model. The system uses an ESP32 to collect sensor data and Python tools to prepare data, train a model, and generate predictions.

## Project overview

The prototype uses:
- **ESP32 DevKit** for sensor interfacing and data collection
- **MQ135** gas sensor for gas-related readings
- **BME280/BMP280** environmental sensor readings, including temperature and pressure
- **Python** for data preparation, model training, visualisation, and prediction

The model workflow uses temperature, pressure, and a gas-reading delta as input features and predicts an estimated number of days to ripeness.

## Features

- Sensor-data logging through the ESP32 workflow
- Baseline-relative gas analysis
- Dataset preparation and merging
- Random Forest regression model
- Graph generation and prediction scripts

## Technology stack

- Python
- pandas
- scikit-learn
- Matplotlib
- ESP32 / Arduino
- MQ135 and BME280/BMP280 sensors

## Repository workflow

Run the scripts from the project directory in the following order:

```bash
python logger.py
python prepare_dataset.py
python train_model.py
```

Use the graph-generation and live-prediction scripts in the repository for their respective workflows:

```bash
python graphs.py
python live_predict.py
```

Install the Python dependencies listed in `requirements.txt` before running the scripts. Hardware-based collection also requires the ESP32 and connected sensors to be configured for the project.

## Model results

The repository's recorded training results are:
- **Mean Absolute Error (MAE):** 0.10
- **R² score:** 0.98

**Important interpretation:** the current dataset-preparation workflow assigns days-to-ripeness labels using gas-delta threshold rules. These scores therefore describe model performance against those prepared labels; they should not be interpreted as proof of accuracy on independently measured, real-world fruit-ripeness outcomes.

## Future improvements

- Validate predictions against independently observed ripening outcomes
- Expand and balance the dataset across fruit types and storage conditions
- Improve calibration and sensor reliability
- Develop a connected dashboard or mobile interface

## Project status

This is a prototype intended for academic demonstration and further experimentation.
