import os
import pandas as pd
import re


def merge_csv_files(data_folder='data', ticker='BTCUSDT'):
    # Initialize an empty list to hold DataFrames and a list to hold dates
    data_frames = []
    dates = []

    # Iterate through all subfolders in the data folder
    for subfolder in os.listdir(data_folder):
        subfolder_path = os.path.join(data_folder, subfolder)

        if os.path.isdir(subfolder_path):
            # List all CSV files in the subfolder
            csv_files = [f for f in os.listdir(subfolder_path) if f.endswith('.csv')]

            # Read each CSV file and append to the list
            for csv_file in csv_files:
                file_path = os.path.join(subfolder_path, csv_file)
                df = pd.read_csv(file_path)
                data_frames.append(df)

                # Extract date from filename using regex
                match = re.search(r'\d{4}-\d{2}-\d{2}', csv_file)
                if match:
                    dates.append(match.group())

    # Concatenate all DataFrames
    merged_df = pd.concat(data_frames)

    # Remove duplicate rows
    merged_df = merged_df.drop_duplicates()

    # Sort dates to find the oldest and newest
    dates.sort()
    oldest_date = dates[0]
    newest_date = dates[-1]

    # Save the merged DataFrame to a CSV file
    output_file = f'{ticker}_{oldest_date}_{newest_date}.csv'
    merged_df.to_csv(output_file, index=False)

    print(f'Merged CSV files from {oldest_date} to {newest_date} and saved as {output_file}')

    return merged_df

def get_latest_merged_csv(data_folder='data'):
    # Get a list of all CSV files in the data folder
    csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

    # Sort the list of CSV files by date
    csv_files.sort()

    # Get the latest CSV file
    latest_csv = csv_files[-1]

    return latest_csv