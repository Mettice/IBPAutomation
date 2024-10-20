import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def create_realistic_mock_data(start_date='2023-01-01', end_date='2023-12-31'):
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    num_days = len(date_range)

    data = {
        'Date': date_range,
        'Sales': np.random.normal(1000, 200, num_days).round().astype(int),
        'Expenses': np.random.normal(800, 150, num_days).round().astype(int),
        'Customer_Satisfaction': np.random.normal(4, 0.5, num_days).clip(1, 5).round(2),
        'Product_A_Units': np.random.poisson(50, num_days),
        'Product_B_Units': np.random.poisson(30, num_days),
        'Product_C_Units': np.random.poisson(20, num_days),
        'Marketing_Spend': np.random.normal(200, 50, num_days).round().astype(int),
    }

    df = pd.DataFrame(data)

    # Add some seasonality
    df['Sales'] = df['Sales'] * (1 + 0.3 * np.sin(np.arange(len(df)) * 2 * np.pi / 365))

    # Add a trend
    df['Sales'] = df['Sales'] * (1 + np.arange(len(df)) * 0.0005)

    # Ensure expenses are always less than sales
    df['Expenses'] = df['Expenses'].clip(upper=df['Sales'] * 0.9)

    return df


# Alias for backward compatibility
create_mock_data = create_realistic_mock_data