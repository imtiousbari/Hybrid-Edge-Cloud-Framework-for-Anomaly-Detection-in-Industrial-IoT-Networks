import os
import subprocess
from flask import Flask, render_template
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
import importlib.util

# test_folder = os.path.join(os.path.dirname(__file__), "Test")

# for filename in os.listdir(test_folder):
#     if filename.endswith(".py"):
#         file_path = os.path.join(test_folder, filename)
#         # Run each script with sudo
#         subprocess.run(["sudo", "python3", file_path])

app = Flask(__name__)
 

@app.route("/")
def dashboard():
    # Load models
    flow_model = joblib.load('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/flow_based_isolation_forest_edge_model.pkl')
    packet_model = joblib.load('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/packet_based_isolation_forest_model.pkl')

    # Load human-readable data for test from dataset_30%

    flow_df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/human_preprocessed_flow_data_30_percent.csv')
    # packet_df_display = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/human_readable_packet_data_web.csv')
    # packet_df_numeric = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/preprocessed_packet_data_web.csv')
   
    # Load numeric (preprocessed) data for model input dataset
    # packet_df_numeric = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/preprocessed_packet_data_web.csv')

    # Load data for test
    # flow_df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Code/Test/network_flows.csv')
    packet_df_display = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Code/Test/network_packets_human.csv')
    packet_df_numeric = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Code/Test/network_packets_numeric.csv')



   
    # Scale numeric data
    scaler = StandardScaler()
    flow_scaled = scaler.fit_transform(flow_df.select_dtypes(include=['int64', 'float64']))
    packet_scaled = scaler.fit_transform(packet_df_numeric)  
    # Predict
    flow_pred = flow_model.predict(flow_scaled)
    packet_pred = packet_model.predict(packet_scaled)

    # Add predictions to display DataFrame
    flow_df['anomaly'] = flow_pred
    packet_df_display['anomaly'] = packet_pred

    flow_df['status'] = flow_df['anomaly'].apply(lambda x: 'anomaly' if x == -1 else 'normal')
    packet_df_display['status'] = packet_df_display['anomaly'].apply(lambda x: 'anomaly' if x == -1 else 'normal')

    # Stats
    total_flow = len(flow_df)
    total_packet = len(packet_df_display)
    flow_count = (flow_pred == -1).sum()
    packet_count = (packet_pred == -1).sum()
    flow_percent = round((flow_count / total_flow) * 100, 2) if total_flow else 0
    packet_percent = round((packet_count / total_packet) * 100, 2) if total_packet else 0

    # Recent data
    recent_flow_anomalies = flow_df[flow_df['status'] == 'anomaly'].tail(5).to_dict(orient='records')
    recent_flow_normals = flow_df[flow_df['status'] == 'normal'].tail(5).to_dict(orient='records')
    recent_packet_anomalies = packet_df_display[packet_df_display['status'] == 'anomaly'].tail(5).to_dict(orient='records')
    recent_packet_normals = packet_df_display[packet_df_display['status'] == 'normal'].tail(5).to_dict(orient='records')

    print("\n=== Flow Predictions ===")
    print(flow_pred)

    print("\n=== Packet Predictions ===")
    print(packet_pred)

    # Print DataFrame heads for inspection
    print("\n=== Flow Data (with predictions) ===")
    print(flow_df.head(10))  # first 10 rows

    print("\n=== Packet Data (with predictions) ===")
    print(packet_df_display.head(10))  # first 10 rows

    # Print anomaly counts and percentages
    print(f"\nFlow anomalies: {flow_count} / {total_flow} ({flow_percent}%)")
    print(f"Packet anomalies: {packet_count} / {total_packet} ({packet_percent}%)")

    # Print recent anomalies
    print("\n=== Recent Flow Anomalies ===")
    print(recent_flow_anomalies)

    print("\n=== Recent Packet Anomalies ===")
    print(recent_packet_anomalies)
    return render_template(
        "dashboard.html",
        flow_count=flow_count,
        packet_count=packet_count,
        total_flow=total_flow,
        total_packet=total_packet,
        flow_percent=flow_percent,
        packet_percent=packet_percent,
        recent_flow_anomalies=recent_flow_anomalies,
        recent_flow_normals=recent_flow_normals,
        recent_packet_anomalies=recent_packet_anomalies,
        recent_packet_normals=recent_packet_normals
    )
# print('total_flow')

if __name__ == "__main__":
    app.run(debug=True)


