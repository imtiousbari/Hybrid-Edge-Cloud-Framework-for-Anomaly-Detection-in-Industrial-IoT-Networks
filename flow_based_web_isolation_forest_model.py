import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/preprocessed_flow_data_web.csv')

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)  

model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
model.fit(scaled_data)

predictions = model.predict(scaled_data)
df['anomaly'] = predictions

df.to_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/flow_with_anomalies.csv', index=False)

joblib.dump(model, '/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/flow_based_isolation_forest_edge_model.pkl')
joblib.dump(scaler, '/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/scaler.pkl')

print("[INFO] Anomalies detected:", (predictions == -1).sum())
print("[INFO] Model and scaler saved.")
