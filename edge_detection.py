

# edge_detection.py
import joblib
import pandas as pd
import time

# === STEP 1: Load Pre-trained Flow-Based Model ===
model_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/flow_based_isolation_forest_edge_model.pkl'
model = joblib.load(model_path)

# === STEP 2: Load Preprocessed Flow Data ===
data_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/preprocessed_flow_data_web.csv'
df = pd.read_csv(data_path)
print(f"[INFO] Loaded flow data shape: {df.shape}")

# === STEP 3: Simulate Real-Time Anomaly Detection ===
print("[INFO] Starting real-time anomaly detection...")
for i, row in df.iterrows():
    data = row.values.reshape(1, -1)
    prediction = model.predict(data)

    if prediction[0] == -1:
        print(f"[ALERT] Anomaly detected at index {i}")
    else:
        print(f"[OK] Normal flow at index {i}")

    time.sleep(1)  # Simulate real-time delay (1 second per flow)
