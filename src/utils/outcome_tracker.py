# src/utils/outcome_tracker.py

import pandas as pd
from datetime import datetime, timedelta


class OutcomeTracker:
    def __init__(self, initial_data):
        self.data = initial_data
        self.start_date = initial_data.index.min()
        self.end_date = initial_data.index.max()
        self.targets = {
            'sales_increase': 0.20,  # 20% increase
            'customer_satisfaction_target': 4.5,
            'customer_satisfaction_timeframe': timedelta(days=180)  # 6 months
        }

    def update_data(self, new_data):
        self.data = pd.concat([self.data, new_data])
        self.end_date = self.data.index.max()

    def calculate_sales_increase(self):
        initial_sales = self.data.loc[self.start_date, 'Sales']
        latest_sales = self.data.loc[self.end_date, 'Sales']
        return (latest_sales - initial_sales) / initial_sales

    def calculate_customer_satisfaction_increase(self):
        initial_satisfaction = self.data.loc[self.start_date, 'Customer_Satisfaction']
        latest_satisfaction = self.data.loc[self.end_date, 'Customer_Satisfaction']
        return latest_satisfaction - initial_satisfaction

    def check_targets(self):
        results = {}

        sales_increase = self.calculate_sales_increase()
        results['sales_increase'] = sales_increase
        results['sales_target_met'] = sales_increase >= self.targets['sales_increase']

        satisfaction_increase = self.calculate_customer_satisfaction_increase()
        results['customer_satisfaction_increase'] = satisfaction_increase
        results['customer_satisfaction_target_met'] = (
                satisfaction_increase >= (self.targets['customer_satisfaction_target'] - self.data.loc[
            self.start_date, 'Customer_Satisfaction']) and
                (self.end_date - self.start_date) <= self.targets['customer_satisfaction_timeframe']
        )

        return results