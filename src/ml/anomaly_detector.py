import numpy as np
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)

    def detect_anomalies(self, data):
        # Prepare features for anomaly detection
        features = data[['Sales', 'Customer_Satisfaction']].values

        # Fit the model and predict
        self.model.fit(features)
        anomalies = self.model.predict(features)

        # Add anomaly detection results to the dataframe
        data['Anomaly'] = anomalies
        return data


# Usage
if __name__ == "__main__":
    from src.utils.data_fetcher import DataFetcher

    fetcher = DataFetcher()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    data = fetcher.fetch_data('MSFT', start_date, end_date)
    processed_data = fetcher.preprocess_data(data)

    detector = AnomalyDetector()
    data_with_anomalies = detector.detect_anomalies(processed_data)
    print(data_with_anomalies[data_with_anomalies['Anomaly'] == -1])  # Print anomalies