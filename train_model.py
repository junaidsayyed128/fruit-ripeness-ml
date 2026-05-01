import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# =========================
# 📌 Function: Convert prediction → stage (ML based)
# =========================
def interpret(days):
    if days >= 5:
        return "Unripe"
    elif days >= 2:
        return "Ripening"
    else:
        return "Ripe"

# =========================
# 📌 Backup rule-based logic (IMPORTANT FIX)
# =========================
def interpret_by_delta(delta):
    if delta < 8:
        return "Unripe"
    elif delta < 30:
        return "Ripening"
    else:
        return "Ripe"

# =========================
# 📌 Load dataset
# =========================
USE_KAGGLE = False   # change True/False as needed

if USE_KAGGLE:
    print("Using merged dataset")
    data = pd.read_csv("final_merged.csv")
else:
    print("Using only sensor dataset")
    data = pd.read_csv("final_data.csv")

X = data[['temperature', 'pressure', 'delta']]
y = data['days_to_ripe']

# =========================
# 📌 Train/Test split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 📌 Train model
# =========================
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# =========================
# 📌 Evaluate model
# =========================
pred = model.predict(X_test)

print("\n========= MODEL PERFORMANCE =========\n")
print("Sample Predictions vs Actual:\n")

for i in range(min(10, len(pred))):
    print(f"Predicted: {round(pred[i],2)} | Actual: {y_test.iloc[i]}")

mae = mean_absolute_error(y_test, pred)
r2  = r2_score(y_test, pred)

print(f"\nMAE: {mae:.2f}")
print(f"R² : {r2:.2f}")

# =========================
# 📌 SINGLE LIVE TEST
# =========================
sample = pd.DataFrame([[34.0, 808.0, 20]],
                      columns=['temperature','pressure','delta'])

pred_value = model.predict(sample)[0]
delta_val = sample['delta'][0]

print("\n========= LIVE PREDICTION =========\n")
print("Temperature:", sample['temperature'][0])
print("Pressure   :", sample['pressure'][0])
print("Delta      :", delta_val)
print("ML Days to ripe:", round(pred_value, 2))
print("ML Stage        :", interpret(pred_value))

# 🔥 IMPORTANT ADDITION
print("Rule-based Stage:", interpret_by_delta(delta_val))

# =========================
# 📌 MULTIPLE TEST CASES
# =========================
print("\n========= DIFFERENT CONDITIONS TEST =========\n")

samples = [
    [33, 807, -5],
    [33, 807, 10],
    [33, 807, 40],
    [33, 807, 200]
]

for s in samples:
    df = pd.DataFrame([s], columns=['temperature','pressure','delta'])
    pred_val = model.predict(df)[0]
    delta = s[2]

    print(f"\nDelta {delta}")
    print(f"ML → {round(pred_val,2)} days → {interpret(pred_val)}")
    print(f"Rule → {interpret_by_delta(delta)}")