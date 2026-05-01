import pandas as pd

# =========================
# 📌 Load Kaggle files
# =========================
d1 = pd.read_csv("Banana D1.csv")
d2 = pd.read_csv("Banana D2.csv")
d3 = pd.read_csv("Banana D3.csv")

# =========================
# 📌 Function to convert gas → delta (NORMALIZATION)
# =========================
def normalize_delta(gas_series):
    mean_val = gas_series.mean()
    std_val = gas_series.std()
    
    # Avoid division by zero
    if std_val == 0:
        std_val = 1

    # Normalize and scale to match your sensor (~ -10 to 60 range)
    normalized = (gas_series - mean_val) / std_val
    scaled = normalized * 20   # adjust scaling if needed

    return scaled

# =========================
# 📌 Process each dataset
# =========================
def process(data, label):
    data = data.rename(columns={"MQ135": "gas"})
    
    # Add dummy env values (same as before)
    data["temperature"] = 33.0
    data["pressure"] = 807.0

    # 🔥 KEY CHANGE: normalize instead of baseline subtraction
    data["delta"] = normalize_delta(data["gas"])

    data["days_to_ripe"] = label

    return data[["temperature", "pressure", "gas", "delta", "days_to_ripe"]]

# =========================
# 📌 Apply processing
# =========================
d1 = process(d1, 6)  # Unripe
d2 = process(d2, 3)  # Ripening
d3 = process(d3, 1)  # Ripe

# Combine Kaggle data
kaggle_data = pd.concat([d1, d2, d3], ignore_index=True)

# =========================
# 📌 Load your real sensor data
# =========================
your_data = pd.read_csv("final_data.csv")

# =========================
# 📌 Merge both datasets
# =========================
final = pd.concat([your_data, kaggle_data], ignore_index=True)

# =========================
# 💾 Save final dataset
# =========================
final.to_csv("final_merged.csv", index=False)

print("✅ Final merged dataset ready (normalized)!")