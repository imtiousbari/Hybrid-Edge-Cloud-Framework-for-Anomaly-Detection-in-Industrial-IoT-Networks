import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif

df_sql = pd.read_csv("SqlInjection.pcap_Flow.csv")
df_upload = pd.read_csv("Uploading_Attack.pcap_Flow.csv")
df_xss = pd.read_csv("XSS.pcap_Flow.csv")

df = pd.concat([df_sql, df_upload, df_xss], ignore_index=True)

df.dropna(inplace=True)

non_numeric_cols = ['Flow ID', 'Src IP', 'Dst IP', 'Timestamp', 'Label']
X = df.drop(columns=non_numeric_cols, errors='ignore')
y = df['Label']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

selector = SelectKBest(score_func=f_classif, k=20)
X_selected = selector.fit_transform(X_scaled, y_encoded)
selected_features = X.columns[selector.get_support(indices=True)]

processed_df = pd.DataFrame(X_selected, columns=selected_features)
processed_df['Label'] = y_encoded

processed_df.to_csv("processed_dataset.csv", index=False)

print("✅ Preprocessing complete. Saved as 'processed_dataset.csv'.")
