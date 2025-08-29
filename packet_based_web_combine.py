import pandas as pd
import os

folder_path = '/Volumes/FileManager/Edge Download/CSCT Project/project/Packet_based_feature_web' 

# List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

df_list = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    df_list.append(df)

# Combine all dataframes
combined_df = pd.concat(df_list, ignore_index=True)

combined_csv_path = os.path.join(folder_path, 'combined_packet_data_web.csv')
combined_df.to_csv(combined_csv_path, index=False)

print(f"Combined dataframe shape: {combined_df.shape}")
print(f"Combined data saved to: {combined_csv_path}")
print(combined_df.head())