import os
import requests
import csv
from datetime import datetime, timedelta
import shutil
import threading


import os
import requests
import csv
from datetime import datetime, timedelta
import threading

class BinanceAPI:
    def __init__(self, pricedata_folder='data'):
        self.pricedata_folder = pricedata_folder

    def download_historical_price_data(self, ticker, start_date, end_date, interval_minutes, progress=True):
        url = "https://api.binance.com/api/v3/klines"

        valid_tickers = self.get_binance_ticker_symbols()
        if ticker not in valid_tickers:
            raise Exception("Invalid ticker symbol")

        output_folder = os.path.join(self.pricedata_folder, f'{ticker}')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if start_date > end_date:
            raise Exception("Start date is after the End date")

        valid_intervals = [3, 5, 15, 30]
        if interval_minutes not in valid_intervals:
            raise Exception(f"This interval: {interval_minutes} isn't available, please use: [1, 3, 5, 15, 30]")

        def download_for_date(current_date):
            start_timestamp = int(current_date.timestamp() * 1000)
            next_date = current_date + timedelta(days=1)
            end_timestamp = int(next_date.timestamp() * 1000)

            parameters = {
                "symbol": ticker,
                "interval": f"{interval_minutes}m",
                "startTime": start_timestamp,
                "endTime": end_timestamp,
                "limit": 1500
            }

            try:
                response = requests.get(url, params=parameters)

                if response.status_code == 200:
                    data = response.json()
                    date_str = current_date.strftime('%Y-%m-%d')
                    filename = f"{ticker}_{date_str}.csv"
                    filepath = os.path.join(output_folder, filename)

                    with open(filepath, 'w', newline='') as file:
                        writer = csv.writer(file)
                        header = ["Timestamp", "Open", "High", "Low", "Close", "Volume", "Kline_Close_Time",
                                  "Quote_Asset_Volume", "Number_of_Trades", "Taker_Buy_Base_Asset_Volume",
                                  "Taker_Buy_Quote_Asset_Volume"]
                        writer.writerow(header)

                        for row in data:
                            timestamp = datetime.fromtimestamp(row[0] / 1000)
                            kline_close_time = datetime.fromtimestamp(row[6] / 1000)
                            modified_row = [timestamp] + row[1:6] + [kline_close_time] + row[7:-1]
                            writer.writerow(modified_row)

                    if progress:
                        print(f"Historische Preisdaten für {ticker} am {date_str} wurden gespeichert.")

            except requests.exceptions.RequestException as e:
                if progress:
                    print(f"Fehler bei der API-Anfrage für {ticker} am {current_date.strftime('%Y-%m-%d')}: {e}")

        current_date = start_date
        threads = []

        while current_date <= end_date:
            thread = threading.Thread(target=download_for_date, args=(current_date,))
            thread.start()
            threads.append(thread)
            current_date += timedelta(days=1)

        for thread in threads:
            thread.join()

    def get_binance_ticker_symbols(self):
        url = 'https://api.binance.com/api/v3/exchangeInfo'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            symbols = [symbol['symbol'] for symbol in data['symbols']]
            return symbols

        except requests.exceptions.RequestException as e:
            print('Error occurred:', e)

class DataDownloader:
    def __init__(self, pricedata_folder='data', progress=True):
        self.progress = progress
        self.pricedata_folder = pricedata_folder
        self.api = BinanceAPI(pricedata_folder)

        if pricedata_folder is not None:
            if not os.path.exists(pricedata_folder):
                os.makedirs(pricedata_folder)

        if pricedata_folder is None:
            self.pricedata_folder = 'data'

    def download_data_for_dates(self, ticker_list, start_date, end_date, interval_minutes):
        if isinstance(ticker_list, str):
            ticker_list = [ticker_list]

        num_threads = min(len(ticker_list), threading.active_count())

        def download_data(ticker):
            self.api.download_historical_price_data(ticker, start_date, end_date, interval_minutes, self.progress)

        threads = []
        for ticker in ticker_list:
            thread = threading.Thread(target=download_data, args=(ticker,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def download_data_for_ndays(self, ticker_list, num_days, interval_minutes):
        if isinstance(ticker_list, str):
            ticker_list = [ticker_list]

        end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - timedelta(days=num_days)

        num_threads = min(len(ticker_list), threading.active_count())

        def download_data(ticker):
            self.api.download_historical_price_data(ticker, start_date, end_date, interval_minutes, self.progress)

        threads = []
        for ticker in ticker_list:
            thread = threading.Thread(target=download_data, args=(ticker,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def get_available_ticker_symbols(self):
        return self.api.get_binance_ticker_symbols()

    def delete_pricedata(self):
        if os.path.exists(self.pricedata_folder):
            shutil.rmtree(self.pricedata_folder)
            print(f"Pricedata deleted")
        else:
            print(f"Pricedata does not exist")


