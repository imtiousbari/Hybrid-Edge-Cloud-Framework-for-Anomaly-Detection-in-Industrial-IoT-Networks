from flask import Flask, render_template
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from scapy.all import sniff, TCP, UDP
import numpy as np

app = Flask(__name__)

# === LOAD MODELS AND SCALERS ===
flow_model = joblib.load('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/flow_based_isolation_forest_edge_model.pkl')
packet_model = joblib.load('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/packet_based_isolation_forest_model.pkl')

flow_scaler = joblib.load('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/scaler.pkl')
packet_scaler = joblib.load('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/packet_scaler.pkl')

# === DEFINE EXACT FEATURE NAMES AND ORDER USED IN TRAINING ===

# IMPORTANT: Replace these lists with exact column names in order from your training data
flow_feature_columns = ['total_packets', 'tcp_count', 'udp_count', 'other_count', 'avg_pkt_length']
packet_feature_columns = ['Dst Port', 'Flow Duration', 'Protocol', 'Src Port', 'Total Bwd packets']

def capture_live_flow_features(duration=5):
    packets = sniff(timeout=duration)
    protocol_counts = {'TCP': 0, 'UDP': 0, 'Other': 0}
    lengths = []

    for pkt in packets:
        lengths.append(len(pkt))
        if TCP in pkt:
            protocol_counts['TCP'] += 1
        elif UDP in pkt:
            protocol_counts['UDP'] += 1
        else:
            protocol_counts['Other'] += 1

    total_packets = len(packets)
    avg_length = np.mean(lengths) if lengths else 0

    flow_features = {
        'total_packets': total_packets,
        'tcp_count': protocol_counts['TCP'],
        'udp_count': protocol_counts['UDP'],
        'other_count': protocol_counts['Other'],
        'avg_pkt_length': avg_length
    }

    df = pd.DataFrame([flow_features])
    # Enforce column order
    df = df[flow_feature_columns]
    return df

@app.route('/')
def dashboard():
    # 1. Capture live flow features
    live_flow_df = capture_live_flow_features()

    # 2. Scale live flow features
    live_flow_scaled = flow_scaler.transform(live_flow_df)

    # 3. Predict live flow anomaly
    live_flow_pred = flow_model.predict(live_flow_scaled)
    live_flow_status = 'Anomaly' if live_flow_pred[0] == -1 else 'Normal'

    # 4. Load samples from saved preprocessed CSVs for dashboard stats
    flow_df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/preprocessed_flow_data_web.csv').sample(100)
    packet_df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/preprocessed_packet_data_web.csv').sample(100)

    # 5. Select & order columns exactly as used in training before scaling
    flow_sample = flow_df[flow_feature_columns]
    packet_sample = packet_df[packet_feature_columns]

    # 6. Scale samples
    flow_scaled = flow_scaler.transform(flow_sample)
    packet_scaled = packet_scaler.transform(packet_sample)

    # 7. Predict anomalies on samples
    flow_pred = flow_model.predict(flow_scaled)
    packet_pred = packet_model.predict(packet_scaled)

    # 8. Add anomaly columns for display
    flow_df['anomaly'] = flow_pred
    packet_df['anomaly'] = packet_pred

    flow_df['status'] = flow_df['anomaly'].apply(lambda x: 'Anomaly' if x == -1 else 'Normal')
    packet_df['status'] = packet_df['anomaly'].apply(lambda x: 'Anomaly' if x == -1 else 'Normal')

    flow_total = len(flow_df)
    packet_total = len(packet_df)
    flow_anomaly_count = (flow_pred == -1).sum()
    packet_anomaly_count = (packet_pred == -1).sum()
    flow_anomaly_percent = round(flow_anomaly_count / flow_total * 100, 2)
    packet_anomaly_percent = round(packet_anomaly_count / packet_total * 100, 2)

    recent_flow_anomalies = flow_df[flow_df['anomaly'] == -1].tail(10).to_dict(orient='records')
    recent_packet_anomalies = packet_df[packet_df['anomaly'] == -1].tail(10).to_dict(orient='records')

    return render_template('dashboard.html',
                           flow_total=flow_total,
                           packet_total=packet_total,
                           flow_anomaly_count=flow_anomaly_count,
                           packet_anomaly_count=packet_anomaly_count,
                           flow_anomaly_percent=flow_anomaly_percent,
                           packet_anomaly_percent=packet_anomaly_percent,
                           recent_flow_anomalies=recent_flow_anomalies,
                           recent_packet_anomalies=recent_packet_anomalies,
                           live_flow_status=live_flow_status)

if __name__ == '__main__':
    app.run(debug=True)
