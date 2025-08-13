# from flask import Flask, render_template
# import pandas as pd
# import joblib
# from sklearn.preprocessing import StandardScaler

# app = Flask(__name__)

# @app.route("/")
# def dashboard():
#     # Load models
#     flow_model = joblib.load('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/flow_based_isolation_forest_edge_model.pkl')
#     packet_model = joblib.load('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/packet_based_isolation_forest_model.pkl')

#     # Load data
#     flow_df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/preprocessed_flow_data_web.csv')
#     packet_df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/preprocessed_packet_data_web.csv')

#     scaler = StandardScaler()

#     # Scale data
#     flow_scaled = scaler.fit_transform(flow_df)
#     packet_scaled = scaler.fit_transform(packet_df)

#     # Predict anomalies (-1 = anomaly)
#     flow_pred = flow_model.predict(flow_scaled)
#     packet_pred = packet_model.predict(packet_scaled)

#     flow_df['anomaly'] = flow_pred
#     packet_df['anomaly'] = packet_pred

#     # Counts and percentages
#     total_flow = len(flow_df)
#     total_packet = len(packet_df)

#     flow_count = (flow_pred == -1).sum()
#     packet_count = (packet_pred == -1).sum()

#     flow_percent = round((flow_count / total_flow) * 100, 2) if total_flow else 0
#     packet_percent = round((packet_count / total_packet) * 100, 2) if total_packet else 0

#     # Recent anomalies (last 5)
#     # recent_flow_anomalies = flow_df[flow_df['anomaly'] == -1].tail(5000).to_dict(orient='records')
#     # recent_packet_anomalies = packet_df[packet_df['anomaly'] == -1].tail(5000).to_dict(orient='records')

#     # Add a new column 'status' with text labels based on 'anomaly' value
#     flow_df['status'] = flow_df['anomaly'].apply(lambda x: 'anomaly' if x == -1 else 'normal')
#     packet_df['status'] = packet_df['anomaly'].apply(lambda x: 'anomaly' if x == -1 else 'normal')

#     # Now you can filter and convert as before, but with the new column included:
#     recent_flow_anomalies = flow_df[flow_df['anomaly'] == -1].tail(5000).to_dict(orient='records')
#     recent_packet_anomalies = packet_df[packet_df['anomaly'] == -1].tail(5000).to_dict(orient='records')


    

#     return render_template("dashboard.html",
#                            flow_count=flow_count,
#                            packet_count=packet_count,
#                            total_flow=total_flow,
#                            total_packet=total_packet,
#                            flow_percent=flow_percent,
#                            packet_percent=packet_percent,
#                            recent_flow_anomalies=recent_flow_anomalies,
#                            recent_packet_anomalies=recent_packet_anomalies)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

@app.route("/")
def dashboard():
    # Load models
    flow_model = joblib.load('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/flow_based_isolation_forest_edge_model.pkl')
    packet_model = joblib.load('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/packet_based_isolation_forest_model.pkl')

    # Load data
    flow_df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web/preprocessed_flow_data_web.csv')
    packet_df = pd.read_csv('/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web/preprocessed_packet_data_web.csv')

    scaler = StandardScaler()

    # Scale data
    flow_scaled = scaler.fit_transform(flow_df)
    packet_scaled = scaler.fit_transform(packet_df)

    # Predict anomalies (-1 = anomaly, 1 = normal)
    flow_pred = flow_model.predict(flow_scaled)
    packet_pred = packet_model.predict(packet_scaled)

    flow_df['anomaly'] = flow_pred
    packet_df['anomaly'] = packet_pred

    # Counts and percentages
    total_flow = len(flow_df)
    total_packet = len(packet_df)

    flow_count = (flow_pred == -1).sum()
    packet_count = (packet_pred == -1).sum()

    flow_percent = round((flow_count / total_flow) * 100, 2) if total_flow else 0
    packet_percent = round((packet_count / total_packet) * 100, 2) if total_packet else 0

    # Status column
    flow_df['status'] = flow_df['anomaly'].apply(lambda x: 'anomaly' if x == -1 else 'normal')
    packet_df['status'] = packet_df['anomaly'].apply(lambda x: 'anomaly' if x == -1 else 'normal')

    # Separate into normal and anomaly lists (last 5000 rows)
    recent_flow_anomalies = flow_df[flow_df['status'] == 'anomaly'].tail(5000).to_dict(orient='records')
    recent_flow_normals = flow_df[flow_df['status'] == 'normal'].tail(5000).to_dict(orient='records')

    recent_packet_anomalies = packet_df[packet_df['status'] == 'anomaly'].tail(5000).to_dict(orient='records')
    recent_packet_normals = packet_df[packet_df['status'] == 'normal'].tail(5000).to_dict(orient='records')

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

if __name__ == "__main__":
    app.run(debug=True)
