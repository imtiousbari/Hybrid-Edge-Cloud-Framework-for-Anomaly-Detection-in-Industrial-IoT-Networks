import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler

# === STEP 1: Combine all CSV files in a folder ===

folder_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web' 

# Get all CSV filenames
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Read and combine CSVs
df_list = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)

# Save combined data
combined_csv_path = os.path.join(folder_path, 'combined_flow_data_web.csv')
combined_df.to_csv(combined_csv_path, index=False)
print(f"[INFO] Combined data saved to: {combined_csv_path}")
print(f"[INFO] Combined shape: {combined_df.shape}")

# === STEP 2: Preprocessing ===

# DEBUG: Show column names
print("[DEBUG] Available columns:")
print(combined_df.columns.tolist())

# ✅ Update based on actual dataset column names
# expected_columns = ['Src Port', 'Dst Port', 'Protocol', 'Tot Fwd Pkts', 'Tot Bwd Pkts', 'Flow Duration']
expected_columns = ['Src Port', 'Dst Port', 'Protocol', 'Total Fwd Packet', 'Total Bwd packets', 'Flow Duration']
# Check if all expected columns exist
missing_cols = [col for col in expected_columns if col not in combined_df.columns]
if missing_cols:
    raise ValueError(f"Missing expected columns: {missing_cols}")

# Filter only relevant columns
df = combined_df[expected_columns].copy()

# Drop rows with missing values
df.dropna(inplace=True)

# Encode 'Protocol' (categorical) to numeric
le_protocol = LabelEncoder()
df['Protocol'] = le_protocol.fit_transform(df['Protocol'])

# Scale numeric features
scaler = StandardScaler()
# numeric_features = ['Src Port', 'Dst Port', 'Tot Fwd Pkts', 'Tot Bwd Pkts', 'Flow Duration']
numeric_features = ['Src Port', 'Dst Port', 'Total Fwd Packet', 'Total Bwd packets', 'Flow Duration']
df[numeric_features] = scaler.fit_transform(df[numeric_features])

# Save preprocessed data
preprocessed_path = os.path.join(folder_path, 'preprocessed_flow_data_web.csv')
df.to_csv(preprocessed_path, index=False)
print(f"[INFO] Preprocessed data saved to: {preprocessed_path}")
print(df.head())
