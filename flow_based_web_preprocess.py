

###########
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler

folder_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web' 

# Step 1: Combine CSV files
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]
combined_df = pd.concat(df_list, ignore_index=True)

combined_csv_path = os.path.join(folder_path, 'combined_flow_data_web.csv')
combined_df.to_csv(combined_csv_path, index=False)
print(f"[INFO] Combined data saved to: {combined_csv_path}")
print(f"[INFO] Combined shape: {combined_df.shape}")
print("[DEBUG] Available columns:")
print(combined_df.columns.tolist())

# Step 2: Preprocess
expected_columns = ['Src Port', 'Dst Port', 'Protocol', 'Total Fwd Packet', 'Total Bwd packets', 'Flow Duration']
missing_cols = [col for col in expected_columns if col not in combined_df.columns]
if missing_cols:
    raise ValueError(f"Missing expected columns: {missing_cols}")

df = combined_df[expected_columns].copy()
df.dropna(inplace=True)

# Label Encoding
le_protocol = LabelEncoder()
df['Protocol'] = le_protocol.fit_transform(df['Protocol'])

# Feature Scaling
scaler = StandardScaler()
numeric_features = ['Src Port', 'Dst Port', 'Total Fwd Packet', 'Total Bwd packets', 'Flow Duration']
df[numeric_features] = scaler.fit_transform(df[numeric_features])

# Save preprocessed data
preprocessed_path = os.path.join(folder_path, 'preprocessed_flow_data_web.csv')
df.to_csv(preprocessed_path, index=False)
print(f"[INFO] Preprocessed data saved to: {preprocessed_path}")

df_human = df.copy()

# Inverse scale numeric features
df_human[numeric_features] = scaler.inverse_transform(df_human[numeric_features])

# Convert Flow Duration to seconds
df_human['Flow Duration'] = (df_human['Flow Duration'] / 1_000_000).round(2)  # 2 decimal places

# Round other numeric features to integers
for col in ['Src Port', 'Dst Port', 'Total Fwd Packet', 'Total Bwd packets']:
    df_human[col] = df_human[col].round().astype(int)

# Convert Protocol back to names
df_human['Protocol'] = le_protocol.inverse_transform(
    df_human['Protocol'].clip(0, len(le_protocol.classes_) - 1)
)

# Save to CSV
human_readable_path = os.path.join(folder_path, 'human_readable_flow_data_web.csv')
df_human.to_csv(human_readable_path, index=False)
print(f"[INFO] Human-readable data saved to: {human_readable_path}")
print(df_human.head())

#  #########


