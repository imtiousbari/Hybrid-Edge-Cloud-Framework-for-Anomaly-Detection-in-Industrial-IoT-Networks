import pandas as pd
import os

folder_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web'

# Load your CSV file
df = pd.read_csv(os.path.join(folder_path, 'preprocessed_flow_data_web.csv'))

# Shuffle the data
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Split the data
split_index = int(0.7 * len(df_shuffled))
df_70 = df_shuffled[:split_index]
df_30 = df_shuffled[split_index:]

# Save to new CSV files
split_path_70 = os.path.join(folder_path, 'preprocessed_flow_data_70_percent.csv')
df_70.to_csv(split_path_70, index=False)
print(f"[INFO] Preprocessed 70% data saved to: {split_path_70}")

split_path_30 = os.path.join(folder_path, 'preprocessed_flow_data_30_percent.csv')
df_30.to_csv(split_path_30, index=False)
print(f"[INFO] Preprocessed 30% data saved to: {split_path_30}")


