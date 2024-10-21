import os
from textblob import TextBlob
from langchain.tools import Tool
import pandas as pd
import matplotlib.pyplot as plt


def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity


sentiment_analysis_tool = Tool(
    name="Sentiment Analysis",
    func=analyze_sentiment,
    description="Analyzes the sentiment of a given text and returns a value between -1 (negative) and 1 (positive)."
)


class SentimentAnalyzer:
    def analyze_feedback(self, feedback_data):
        feedback_data['Sentiment'] = feedback_data['Feedback'].apply(analyze_sentiment)
        return feedback_data

    def plot_sentiment_trend(self, feedback_data):
        sentiment_over_time = feedback_data.groupby('Date')['Sentiment'].mean().reset_index()

        plt.figure(figsize=(12, 6))
        plt.plot(sentiment_over_time['Date'], sentiment_over_time['Sentiment'])
        plt.title('Customer Sentiment Trend')
        plt.xlabel('Date')
        plt.ylabel('Average Sentiment')
        plt.ylim(-1, 1)

        # Create 'static' directory if it doesn't exist
        os.makedirs('static', exist_ok=True)

        plt.savefig('static/sentiment_trend.png')
        plt.close()


# Usage example
if __name__ == "__main__":
    # Mock customer feedback data
    feedback_data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=100),
        'Feedback': [
                        "Great product!",
                        "Not satisfied with the service.",
                        "Could be better.",
                        "Excellent customer support!",
                        "Product arrived damaged."
                    ] * 20
    })

    analyzer = SentimentAnalyzer()
    analyzed_feedback = analyzer.analyze_feedback(feedback_data)
    analyzer.plot_sentiment_trend(analyzed_feedback)
    print("Sentiment trend plot saved as 'static/sentiment_trend.png'")
    print(analyzed_feedback.head())