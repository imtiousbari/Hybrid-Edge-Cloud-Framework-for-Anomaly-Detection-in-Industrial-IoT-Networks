# import pandas as pd
# import os
# from sklearn.ensemble import IsolationForest
# import joblib  # Needed to save the model as .pkl

# # === STEP 1: Load Preprocessed Data ===
# folder_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web'
# input_file = os.path.join(folder_path, 'preprocessed_packet_data_web.csv')

# df = pd.read_csv(input_file)
# print(f"[INFO] Loaded preprocessed data with shape: {df.shape}")

# # === STEP 2: Fit Isolation Forest Model ===
# model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
# model.fit(df)

# # === STEP 3: Predict Anomalies ===
# df['anomaly'] = model.predict(df)
# df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})

# # === STEP 4: Save Results as .pkl ===
# result_pkl = os.path.join(folder_path, 'anomaly_detection_results.pkl')
# df.to_pickle(result_pkl)
# print(f"[INFO] Anomaly detection results saved as pickle file to: {result_pkl}")

# # Optional: Save the trained model as .pkl too
# model_pkl = os.path.join(folder_path, 'packet_based_isolation_forest_model.pkl')
# joblib.dump(model, model_pkl)
# print(f"[INFO] Trained Isolation Forest model saved as: {model_pkl}")

# # === STEP 5: Summary ===
# anomaly_count = df['anomaly'].value_counts()
# print(f"[INFO] Anomaly summary:\n{anomaly_count}")


import pandas as pd
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# === STEP 1: Load Preprocessed Data ===
folder_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web'
input_file = os.path.join(folder_path, 'preprocessed_packet_data_web.csv')

df = pd.read_csv(input_file)
print(f"[INFO] Loaded preprocessed data with shape: {df.shape}")

# === STEP 2: Fit StandardScaler and transform data ===
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# === STEP 3: Fit Isolation Forest Model on scaled data ===
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
model.fit(scaled_data)

# === STEP 4: Predict Anomalies ===
df['anomaly'] = model.predict(scaled_data)
df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})

# === STEP 5: Save Results as .pkl ===
result_pkl = os.path.join(folder_path, 'anomaly_detection_results.pkl')
df.to_pickle(result_pkl)
print(f"[INFO] Anomaly detection results saved as pickle file to: {result_pkl}")

# === STEP 6: Save the trained model and scaler ===
model_pkl = os.path.join(folder_path, 'packet_based_isolation_forest_model.pkl')
scaler_pkl = os.path.join(folder_path, 'packet_scaler.pkl')
joblib.dump(model, model_pkl)
joblib.dump(scaler, scaler_pkl)
print(f"[INFO] Trained Isolation Forest model saved as: {model_pkl}")
print(f"[INFO] StandardScaler saved as: {scaler_pkl}")

# === STEP 7: Summary ===
anomaly_count = df['anomaly'].value_counts()
print(f"[INFO] Anomaly summary:\n{anomaly_count}")
