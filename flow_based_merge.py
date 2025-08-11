import os
import pandas as pd

flow_data_folder = "/Volumes/FileManager/Edge Download/CSCT Project/project/Flow_based_web"

dataframes = []

for filename in os.listdir(flow_data_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(flow_data_folder, filename)
        try:
            df = pd.read_csv(file_path)
            label = filename.split('_')[0] 
            df['label'] = label
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

if dataframes:
    merged_df = pd.concat(dataframes, ignore_index=True)
    merged_df.to_csv("flow_merged.csv", index=False)
    print("Merged flow-based dataset saved as 'flow_merged.csv'")
else:
    print("No CSV files found or failed to read.")


   