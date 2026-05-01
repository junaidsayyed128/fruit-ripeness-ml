import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load data
USE_KAGGLE = False

if USE_KAGGLE:
    data = pd.read_csv("final_merged.csv")
else:
    data = pd.read_csv("final_data.csv")
X = data[['temperature', 'pressure', 'delta']]
y = data['days_to_ripe']

# Train model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

# =========================
# 📈 GRAPH 1: Actual vs Predicted
# =========================
plt.figure(figsize=(7,5))

# Color mapping
colors = []
for val in y_test:
    if val >= 5:
        colors.append('green')   # Unripe
    elif val >= 2:
        colors.append('orange')  # Ripening
    else:
        colors.append('red')     # Ripe

plt.scatter(y_test, predictions, c=colors)

# Perfect prediction line
plt.plot([0, 7], [0, 7], linestyle='--', label="Perfect Prediction")

# Trend line
z = np.polyfit(y_test, predictions, 1)
p = np.poly1d(z)
plt.plot(y_test, p(y_test), label="Trend Line")

plt.xlabel("Actual Days to Ripeness")
plt.ylabel("Predicted Days")
plt.title("Actual vs Predicted Ripeness")
plt.legend()
plt.grid()

# Save figure
plt.savefig("Figure_1_Research.png", dpi=300)
plt.show()

# =========================
# 📈 GRAPH 2: Gas vs Ripeness
# =========================
plt.figure(figsize=(7,5))

# Color coding for full dataset
colors = []
for val in data['days_to_ripe']:
    if val >= 5:
        colors.append('green')
    elif val >= 2:
        colors.append('orange')
    else:
        colors.append('red')

plt.scatter(data['delta'], data['days_to_ripe'], c=colors)

# Trend line
z = np.polyfit(data['delta'], data['days_to_ripe'], 1)
p = np.poly1d(z)
plt.plot(data['delta'], p(data['delta']), label="Trend Line")

plt.xlabel("Gas Delta (Baseline Corrected)")
plt.ylabel("Days to Ripeness")
plt.title("Gas Emission vs Ripeness")
plt.legend()
plt.grid()

# Save figure
plt.savefig("Figure_2_Research.png", dpi=300)
plt.show()