import serial
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# =========================
# 📌 LOAD DATA + TRAIN MODEL
# =========================
data = pd.read_csv("final_data.csv")

X = data[['temperature', 'pressure', 'delta']]
y = data['days_to_ripe']

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

# =========================
# 📌 INTERPRETATION FUNCTION
# =========================
def interpret(days):
    if days >= 5:
        return "Unripe"
    elif days >= 2:
        return "Ripening"
    else:
        return "Ripe"

# =========================
# 📌 SERIAL CONNECTION
# =========================
ser = serial.Serial('COM3', 115200)
print("🔄 Waiting for clean sensor data...\n")

# =========================
# 📌 SMOOTHING + PEAK
# =========================
delta_buffer = []
BUFFER_SIZE = 10   # smoother
max_delta = 0      # 🔥 peak hold

while True:
    try:
        line = ser.readline().decode(errors='ignore').strip()

        # ❌ Ignore calibration/debug lines
        if not line or "Reading" in line or "Baseline" in line or "Calibrating" in line:
            continue

        if "," in line:
            values = line.split(',')

            if len(values) == 4:
                try:
                    temp = float(values[0])
                    pres = float(values[1])
                    gas  = float(values[2])
                    delta = float(values[3])
                except:
                    continue

                # ❌ Ignore garbage spikes
                if abs(delta) > 300:
                    continue

                # =========================
                # 📌 SMOOTHING
                # =========================
                delta_buffer.append(delta)

                if len(delta_buffer) > BUFFER_SIZE:
                    delta_buffer.pop(0)

                smooth_delta = sum(delta_buffer) / len(delta_buffer)

                # =========================
                # 🔥 PEAK HOLD
                # =========================
                if smooth_delta > max_delta:
                    max_delta = smooth_delta

                # =========================
                # 📌 ML Prediction (USE PEAK)
                # =========================
                sample = pd.DataFrame([[temp, pres, max_delta]],
                                      columns=['temperature','pressure','delta'])

                pred = model.predict(sample)[0]

                # =========================
                # 📌 OUTPUT
                # =========================
                print("=================================")
                print(f"Temp          : {round(temp,2)} °C")
                print(f"Delta (live)  : {round(smooth_delta,2)}")
                print(f"Delta (peak)  : {round(max_delta,2)}")
                print(f"Days          : {round(pred,2)}")
                print(f"Stage         : {interpret(pred)}")

                # Demo-friendly message
                if max_delta < 5:
                    print("Status        : Clean air / No fruit")
                elif max_delta < 30:
                    print("Status        : Mild ripening detected")
                else:
                    print("Status        : Strong ripening (fruit nearby)")

                print("=================================\n")

    except KeyboardInterrupt:
        print("\n🛑 Stopped.")
        break