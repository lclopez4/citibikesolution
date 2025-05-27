import pandas as pd
import os

# Set the path to your folder with Citi Bike data
input_folder = '.'
output_folder = './Citi_Bike_Cleaned'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all CSV files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        filepath = os.path.join(input_folder, filename)

        try:
            # Load the CSV file
            df = pd.read_csv(filepath)

            # Try to find and parse the datetime column
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

            # Save the updated CSV to the output folder
            output_path = os.path.join(output_folder, filename)
            df.to_csv(output_path, index=False)
            print(f"✅ Processed: {filename}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
