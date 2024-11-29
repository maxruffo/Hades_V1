import os
import logging
from datetime import datetime
import pandas as pd
from src.main.data_preprocessing.data_utils import merge_csv_files
from src.main.data_preprocessing.calc_tradingsignals import calc_trading_indicators
from src.main.data_preprocessing.binance_utils import DataDownloader
import json
def load_config(config_file='config.json'):
    with open(config_file, 'r') as file:
        config = json.load(file)
    config['START_DATE'] = datetime.strptime(config['START_DATE'], '%Y-%m-%d')
    config['END_DATE'] = datetime.strptime(config['END_DATE'], '%Y-%m-%d')
    return config

def set_config(ticker, start_date, end_date, interval_minutes, config_file='config.json'):
    config = {
        "TICKER": ticker,
        "START_DATE": start_date.strftime('%Y-%m-%d'),
        "END_DATE": end_date.strftime('%Y-%m-%d'),
        "INTERVAL_MINUTES": interval_minutes
    }
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)

def format_config(config):
    config_str = json.dumps({
        "TICKER": config['TICKER'],
        "START_DATE": config['START_DATE'].strftime('%Y-%m-%d'),
        "END_DATE": config['END_DATE'].strftime('%Y-%m-%d'),
        "INTERVAL_MINUTES": config['INTERVAL_MINUTES']
    }, indent=4)
    return config_str


def get_training_data(config):
    # Create the output directory if it doesn't exist
    output_dir = os.path.join('data', 'training_data', config['TICKER'])
    os.makedirs(output_dir, exist_ok=True)

    # Define the output file name
    output_file = os.path.join(output_dir, f"{config['TICKER']}_{config['START_DATE'].strftime('%Y-%m-%d')}_{config['END_DATE'].strftime('%Y-%m-%d')}_{config['INTERVAL_MINUTES']}.csv")

    # Check if the file already exists
    if os.path.exists(output_file):
        # Load the data from the file
        df = pd.read_csv(output_file)
        print()
        print("Data loaded from file")
        # print rows number
        return output_file

    # Download historical price data
    downloader = DataDownloader()
    downloader.download_data_for_dates(config['TICKER'], config['START_DATE'], config['END_DATE'], config['INTERVAL_MINUTES'])

    # Merge CSV files
    merged_df = merge_csv_files()

    # Calculate trading indicators
    merged_df_with_indicators = calc_trading_indicators(merged_df)

    # Save the DataFrame to a CSV file
    merged_df_with_indicators.to_csv(output_file, index=False)
    print("Data saved to file")
    print(len(merged_df_with_indicators))
    return output_file
def main():
    config = load_config()
    logging.basicConfig(level=logging.INFO)
    print("This is your current CONFIGURATION:")
    print(format_config(config))

    # Ask if you want to change the config
    change_config = input("Do you want to change the config? (y/n): ")
    if change_config.lower() == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        ticker = input("Enter the ticker: ")
        start_date = datetime.strptime(input("Enter the start date (yyyy-mm-dd): "), '%Y-%m-%d')
        end_date = datetime.strptime(input("Enter the end date (yyyy-mm-dd): "), '%Y-%m-%d')
        interval_minutes = int(input("Enter the interval in minutes: "))
        set_config(ticker, start_date, end_date, interval_minutes)
        config = load_config()
        print("This is your New Config:")
        print(format_config(config))

    training_data = get_training_data(config)

    print("You can find the Training Data for your Ticker under this path:")
    print(training_data)

if __name__ == '__main__':
    main()
