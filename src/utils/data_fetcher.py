import requests
import pandas as pd
from datetime import datetime, timedelta
import os


class DataFetcher:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not self.api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY environment variable is not set")
        self.base_url = 'https://www.alphavantage.co/query'

    def fetch_data(self, symbol, start_date, end_date):
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.api_key,
            'outputsize': 'full'
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()

            if 'Error Message' in data:
                raise ValueError(f"API Error: {data['Error Message']}")

            if 'Time Series (Daily)' not in data:
                print("Full API Response:", data)  # For debugging
                raise KeyError("'Time Series (Daily)' not found in API response")

            time_series = data['Time Series (Daily)']
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            df = df.loc[start_date:end_date]
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            df = df.astype(float)
            return df
        except requests.RequestException as e:
            print(f"HTTP Request failed: {e}")
            # Return some mock data for demonstration purposes
            return self.create_mock_data(start_date, end_date)
        except (KeyError, ValueError) as e:
            print(f"Data processing error: {e}")
            return self.create_mock_data(start_date, end_date)

    def create_mock_data(self, start_date, end_date):
        print("Creating mock data due to API fetch failure")
        date_range = pd.date_range(start=start_date, end=end_date)
        mock_data = pd.DataFrame({
            'Open': np.random.uniform(100, 200, len(date_range)),
            'High': np.random.uniform(120, 220, len(date_range)),
            'Low': np.random.uniform(80, 180, len(date_range)),
            'Close': np.random.uniform(90, 210, len(date_range)),
            'Volume': np.random.randint(1000000, 10000000, len(date_range))
        }, index=date_range)
        return mock_data

    def preprocess_data(self, data):
        data['Date'] = data.index
        data['Sales'] = data['Close'] * data['Volume']  # Simulating sales data
        data['Customer_Satisfaction'] = (data['Close'] - data['Open']) / data[
            'Open'] + 3  # Simulating customer satisfaction
        return data


# Usage
if __name__ == "__main__":
    fetcher = DataFetcher()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    data = fetcher.fetch_data('MSFT', start_date, end_date)
    processed_data = fetcher.preprocess_data(data)
    print(processed_data.head())