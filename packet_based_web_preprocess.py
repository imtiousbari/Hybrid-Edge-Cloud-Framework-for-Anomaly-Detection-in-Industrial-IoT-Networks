import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Folder containing CSV files
folder_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web'

# List CSV files
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
if not csv_files:
    raise FileNotFoundError(f"No CSV files found in folder: {folder_path}")

# Load all CSV files
df_list = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    try:
        df = pd.read_csv(file_path, low_memory=False)  
        df_list.append(df)
        print(f"[INFO] Loaded {file} with shape {df.shape}")
    except Exception as e:
        print(f"[ERROR] Failed to load {file}: {e}")

# Combine all data
combined_df = pd.concat(df_list, ignore_index=True)
print(f"[INFO] Combined shape: {combined_df.shape}")

# Show available columns
print("[DEBUG] Available columns:")
print(combined_df.columns.tolist())

# Select relevant numerical features
selected_columns = [
    'flow_duration', 'payload_length', 'inter_arrival_time', 'tcp_window_size',
    'jitter', 'stream_1_mean', 'stream_1_var', 'src_ip_1_mean', 'src_ip_1_var',
    'stream_5_mean', 'src_ip_5_var', 'stream_10_var',
    'stream_30_var', 'src_ip_60_var', 'channel_1_mean'
]

selected_columns = [col for col in selected_columns if col in combined_df.columns]
if not selected_columns:
    raise ValueError("None of the selected numerical features found in dataset.")

# Prepare DataFrame
df = combined_df[selected_columns].copy()
df.dropna(inplace=True)

# Add protocol column if available
if 'l4_tcp' in combined_df.columns and 'l4_udp' in combined_df.columns:
    df['protocol'] = combined_df.apply(
        lambda row: 'TCP' if row['l4_tcp'] == 1 else ('UDP' if row['l4_udp'] == 1 else 'OTHER'), axis=1
    )
    # ✅ Ensure protocol is treated as string before encoding
    le = LabelEncoder()
    df['protocol'] = le.fit_transform(df['protocol'].astype(str))

# --- SCALE ONLY NUMERIC COLUMNS ---
print("[DEBUG] Data types before scaling:")
print(df.dtypes)

# ✅ Select only numeric columns
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
non_numeric_cols = df.select_dtypes(exclude=['float64', 'int64']).columns

scaler = StandardScaler()
df_scaled_numeric = pd.DataFrame(scaler.fit_transform(df[numeric_cols]), columns=numeric_cols)

# Combine scaled numeric data with non-numeric columns
df_scaled = pd.concat([df_scaled_numeric, df[non_numeric_cols].reset_index(drop=True)], axis=1)

# Function to convert snake_case to Title Case
def snake_to_title(name):
    return name.replace('_', ' ').title()

df_scaled.rename(columns={col: snake_to_title(col) for col in df_scaled.columns}, inplace=True)

# Save ML-ready scaled CSV
preprocessed_path = os.path.join(folder_path, 'preprocessed_packet_data_web.csv')
df_scaled.to_csv(preprocessed_path, index=False)
print(f"[INFO] Preprocessed (scaled) data saved to: {preprocessed_path}")
print(df_scaled.head())

# --- SAVE HUMAN-READABLE CSV ---
human_readable_path = os.path.join(folder_path, 'human_readable_packet_data_web.csv')
df_human = combined_df[selected_columns].copy()
df_human.dropna(inplace=True)

# Add protocol column for human-readable CSV
if 'l4_tcp' in combined_df.columns and 'l4_udp' in combined_df.columns:
    df_human['Protocol'] = combined_df.apply(
        lambda row: 'TCP' if row['l4_tcp'] == 1 else ('UDP' if row['l4_udp'] == 1 else 'OTHER'), axis=1
    )

# Rename columns to human-readable
df_human.rename(columns={col: snake_to_title(col) for col in df_human.columns}, inplace=True)

# Save human-readable CSV
df_human.to_csv(human_readable_path, index=False)
print(f"[INFO] Human-readable data saved to: {human_readable_path}")
print(df_human.head())


# import pandas as pd
# import os
# from sklearn.preprocessing import LabelEncoder, StandardScaler

# # === STEP 1: Combine all CSV files ===
# folder_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web'

# csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
# if not csv_files:
#     raise FileNotFoundError(f"No CSV files found in folder: {folder_path}")

# df_list = []
# for file in csv_files:
#     file_path = os.path.join(folder_path, file)
#     try:
#         df = pd.read_csv(file_path, low_memory=False)  # suppress dtype warning
#         df_list.append(df)
#         print(f"[INFO] Loaded {file} with shape {df.shape}")
#     except Exception as e:
#         print(f"[ERROR] Failed to load {file}: {e}")

# combined_df = pd.concat(df_list, ignore_index=True)
# print(f"[INFO] Combined shape: {combined_df.shape}")

# # === STEP 2: Select useful numerical features ===

# # Print column names for inspection
# print("[DEBUG] Available columns:")
# print(combined_df.columns.tolist())

# # Choose numerical features suitable for anomaly detection
# selected_columns = [
#     'flow_duration', 'payload_length', 'inter_arrival_time', 'tcp_window_size',
#     'jitter', 'stream_1_mean', 'stream_1_var', 'src_ip_1_mean', 'src_ip_1_var',
#     'stream_5_mean', 'src_ip_5_var', 'stream_10_var',
#     'stream_30_var', 'src_ip_60_var', 'channel_1_mean'
# ]

# # Filter existing columns only
# selected_columns = [col for col in selected_columns if col in combined_df.columns]
# if not selected_columns:
#     raise ValueError("None of the selected numerical features found in dataset.")

# df = combined_df[selected_columns].copy()
# df.dropna(inplace=True)

# # === STEP 3: Add protocol feature (optional) ===
# if 'l4_tcp' in combined_df.columns and 'l4_udp' in combined_df.columns:
#     df['protocol'] = combined_df.apply(
#         lambda row: 'TCP' if row['l4_tcp'] == 1 else ('UDP' if row['l4_udp'] == 1 else 'OTHER'), axis=1
#     )
#     df['protocol'] = LabelEncoder().fit_transform(df['protocol'])

# # === STEP 4: Normalize (scale) all features ===
# scaler = StandardScaler()
# df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

# # === STEP 5: Save preprocessed dataset ===
# preprocessed_path = os.path.join(folder_path, 'preprocessed_packet_data_web.csv')
# df_scaled.to_csv(preprocessed_path, index=False)
# print(f"[INFO] Preprocessed data saved to: {preprocessed_path}")
# print(df_scaled.head())