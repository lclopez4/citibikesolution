# %% Import Libraries
import pandas as pd
import os

# %% Step 1: Clean individual files and save to output folder
input_folder = '.'
output_folder = './Citi_Bike_Cleaned'
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        filepath = os.path.join(input_folder, filename)

        try:
            df = pd.read_csv(filepath)

            if 'started_at' in df.columns:
                df['started_at'] = pd.to_datetime(df['started_at'], errors='coerce')
                df['year'] = df['started_at'].dt.year
                df['month_year'] = df['started_at'].dt.to_period('M').astype(str)
            elif 'starttime' in df.columns:
                df['starttime'] = pd.to_datetime(df['starttime'], errors='coerce')
                df['year'] = df['starttime'].dt.year
                df['month_year'] = df['starttime'].dt.to_period('M').astype(str)
            else:
                print(f"⚠️ Date column not found in {filename}. Skipping.")
                continue

            output_path = os.path.join(output_folder, filename)
            df.to_csv(output_path, index=False)
            print(f"✅ Processed: {filename}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

# %% Step 2: Merge cleaned files
folder_path = './Citi_Bike_Cleaned'
combined_df = pd.DataFrame()

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

# %% Step 3: Clean and filter for 2019–2021
combined_df = combined_df.dropna(axis=1, how='all')
combined_df = combined_df.loc[:, ~combined_df.columns.str.contains('^Unnamed')]
combined_df = combined_df[(combined_df['year'] >= 2019) & (combined_df['year'] <= 2021)]

# %% Step 4: Take a sample for Tableau (100k rows)
sample_df = combined_df.sample(n=100000, random_state=42)

# %% Step 5: Save sample file
sample_df.to_csv('Citi_Bike_Sample.csv', index=False, encoding='utf-8', lineterminator='\n')
print("✅ Sample file saved as 'Citi_Bike_Sample.csv'")

# %% Step 6: Run sanity checks
print(sample_df.shape)
print(sample_df.columns)
print(sample_df.head())
