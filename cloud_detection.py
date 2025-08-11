# # cloud_detection.py
# import pickle
# import pandas as pd
# from sklearn.preprocessing import StandardScaler

# # Load model
# with open('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/packet_based_isolation_forest_model.pkl', 'rb') as f:
#     model = pickle.load(f)

# # Load packet-level test data
# df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/preprocessed_packet_data_web.csv')  # Preprocessed packet features

# # Scale if necessary
# scaler = StandardScaler()
# df_scaled = scaler.fit_transform(df)

# # Predict
# predictions = model.predict(df_scaled)

# # Summary
# anomalies = (predictions == -1).sum()
# print(f"Total packets: {len(df)}, Anomalies: {anomalies}")


# cloud_detection.py
import pickle
import pandas as pd
import joblib  # Better than pickle for sklearn models

# === STEP 1: Load Pre-trained Model ===
model_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/packet_based_isolation_forest_model.pkl'
model = joblib.load(model_path)

# === STEP 2: Load Packet-Level Preprocessed Data ===
data_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/preprocessed_packet_data_web.csv'
df = pd.read_csv(data_path)
print(f"[INFO] Loaded test data shape: {df.shape}")

# === STEP 3: Predict Using Model (No Scaling Needed If Not Used in Training) ===
predictions = model.predict(df)

# === STEP 4: Convert Predictions to 0 (normal) and 1 (anomaly)
df['anomaly'] = [1 if pred == -1 else 0 for pred in predictions]

# === STEP 5: Print Anomaly Summary ===
anomalies = df['anomaly'].sum()
print(f"[INFO] Total packets: {len(df)}")
print(f"[INFO] Anomalies detected: {anomalies}")
print(f"[INFO] Normal packets: {len(df) - anomalies}")

# === (Optional) Save Prediction Results for Cloud Dashboard ===
output_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/cloud_detected_anomalies.csv'
df.to_csv(output_path, index=False)
print(f"[INFO] Results saved to: {output_path}")
