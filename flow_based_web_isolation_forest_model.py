import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Load preprocessed data
df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/preprocessed_flow_data_web.csv')

# Train Isolation Forest (unsupervised)
model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
model.fit(df)

# Predict anomalies (-1 = anomaly, 1 = normal)
predictions = model.predict(df)
df['anomaly'] = predictions

# Save predictions for evaluation or dashboard
df.to_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/flow_with_anomalies.csv', index=False)

# Save model for edge deployment
joblib.dump(model, '/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/flow_based_isolation_forest_edge_model.pkl')

# Optional: Print anomaly count
print("[INFO] Anomalies detected:", (predictions == -1).sum())
print("[INFO] Model and results saved.")
