import pandas as pd

# =========================
# 📌 Load data
# =========================
data = pd.read_csv("fruit_data.csv")

# Remove header rows accidentally logged
data = data[data['delta'] != 'delta']

# =========================
# 📌 Convert to numeric safely
# =========================
cols = ['temperature', 'pressure', 'gas', 'delta']
for c in cols:
    data[c] = pd.to_numeric(data[c], errors='coerce')

data = data.dropna()

# =========================
# 📌 OPTIONAL: clip extreme noise (helps stability)
# =========================
data = data[(data['delta'] > -1000) & (data['delta'] < 500)]

# =========================
# 📌 IMPROVED LABELING (TIGHTER RANGES)
# =========================
def assign_days(delta):
    # tune these for your calibrated baseline
    if delta < 8:
        return 6      # Unripe
    elif delta < 30:
        return 3      # Ripening
    else:
        return 1      # Ripe

data['days_to_ripe'] = data['delta'].apply(assign_days)

# =========================
# 📊 Check distribution (VERY IMPORTANT)
# =========================
print("\nLabel distribution:")
print(data['days_to_ripe'].value_counts())

# =========================
# 💾 Save
# =========================
data.to_csv("final_data.csv", index=False)

print("\n✅ Dataset cleaned and saved as final_data.csv")