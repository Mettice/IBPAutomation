import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


class SalesForecaster:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def prepare_data(self, data):
        data['Day'] = data['Date'].dt.day
        data['Month'] = data['Date'].dt.month
        data['Year'] = data['Date'].dt.year
        return data

    def train(self, data):
        prepared_data = self.prepare_data(data)
        X = prepared_data[['Day', 'Month', 'Year']]
        y = prepared_data['Sales']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Model MSE: {mse}")

    def forecast(self, future_dates):
        future_data = pd.DataFrame({'Date': future_dates})
        prepared_data = self.prepare_data(future_data)
        X_future = prepared_data[['Day', 'Month', 'Year']]
        return self.model.predict(X_future)

    def plot_forecast(self, historical_data, future_dates, forecasted_sales):
        plt.figure(figsize=(12, 6))
        plt.plot(historical_data['Date'], historical_data['Sales'], label='Historical Sales')
        plt.plot(future_dates, forecasted_sales, label='Forecasted Sales', linestyle='--')
        plt.title('Sales Forecast')
        plt.xlabel('Date')
        plt.ylabel('Sales')
        plt.legend()
        plt.savefig('static/sales_forecast.png')
        plt.close()


# Usage
if __name__ == "__main__":
    from src.utils.data_fetcher import DataFetcher

    api_url = "https://api.example.com/business_data"  # Replace with actual API URL
    fetcher = DataFetcher(api_url)

    end_date = pd.Timestamp.now()
    start_date = end_date - pd.Timedelta(days=365)

    data = fetcher.fetch_data(start_date, end_date)
    processed_data = fetcher.preprocess_data(data)

    forecaster = SalesForecaster()
    forecaster.train(processed_data)

    future_dates = pd.date_range(start=end_date, periods=30)
    forecasted_sales = forecaster.forecast(future_dates)

    forecaster.plot_forecast(processed_data, future_dates, forecasted_sales)
    print("Forecast plot saved as 'sales_forecast.png'")