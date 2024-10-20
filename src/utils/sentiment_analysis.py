# src/utils/sentiment_analysis.py

from textblob import TextBlob
from langchain.tools import Tool

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns a value between -1 (negative) and 1 (positive)

sentiment_analysis_tool = Tool(
    name="Sentiment Analysis",
    func=analyze_sentiment,
    description="Analyzes the sentiment of a given text and returns a value between -1 (negative) and 1 (positive)."
)