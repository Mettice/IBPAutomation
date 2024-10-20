import pandas as pd
import numpy as np

def create_mock_data():
    data = {
        'Date': pd.date_range(start='2023-01-01', end='2023-12-31', freq='D'),
        'Sales': np.random.randint(100, 1000, 365),
        'Expenses': np.random.randint(50, 500, 365),
        'Customer_Satisfaction': np.random.uniform(3, 5, 365)
    }
    return pd.DataFrame(data)