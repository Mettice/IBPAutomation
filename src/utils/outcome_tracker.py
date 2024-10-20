# src/utils/outcome_tracker.py

import pandas as pd
from datetime import datetime, timedelta


class OutcomeTracker:
    def __init__(self, initial_data):
        self.data = initial_data
        self.start_date = initial_data['Date'].min()
        self.end_date = initial_data['Date'].max()
        self.targets = {
            'underperforming_product_sales_increase': 0.20,  # 20% increase
            'customer_satisfaction_target': 4.5,
            'customer_satisfaction_timeframe': timedelta(days=180)  # 6 months
        }

    def update_data(self, new_data):
        self.data = pd.concat([self.data, new_data])
        self.end_date = self.data['Date'].max()

    def calculate_product_sales_increase(self, product):
        initial_sales = self.data[self.data['Date'] == self.start_date][f'Product_{product}_Units'].values
        latest_sales = self.data[self.data['Date'] == self.end_date][f'Product_{product}_Units'].values

        if len(initial_sales) == 0 or len(latest_sales) == 0:
            return 0  # Return 0 if we don't have the data to calculate

        return (latest_sales[0] - initial_sales[0]) / initial_sales[0]

    def calculate_customer_satisfaction_increase(self):
        initial_satisfaction = self.data[self.data['Date'] == self.start_date]['Customer_Satisfaction'].values
        latest_satisfaction = self.data[self.data['Date'] == self.end_date]['Customer_Satisfaction'].values

        if len(initial_satisfaction) == 0 or len(latest_satisfaction) == 0:
            return 0  # Return 0 if we don't have the data to calculate

        return latest_satisfaction[0] - initial_satisfaction[0]

    def check_targets(self):
        results = {}
        for product in ['A', 'B', 'C']:
            increase = self.calculate_product_sales_increase(product)
            results[f'Product_{product}_sales_increase'] = increase
            results[f'Product_{product}_target_met'] = increase >= self.targets[
                'underperforming_product_sales_increase']

        satisfaction_increase = self.calculate_customer_satisfaction_increase()
        results['customer_satisfaction_increase'] = satisfaction_increase
        results['customer_satisfaction_target_met'] = (
                satisfaction_increase >= (
                    self.targets['customer_satisfaction_target'] - self.data['Customer_Satisfaction'].iloc[0]) and
                (self.end_date - self.start_date) <= self.targets['customer_satisfaction_timeframe']
        )

        return results