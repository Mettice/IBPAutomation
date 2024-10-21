# main.py

from crewai import Crew
from src.utils.data_utils import create_realistic_mock_data
from src.utils.outcome_tracker import OutcomeTracker
from src.agents.agents import (
    create_data_analyst, create_process_optimizer,
    create_automation_engineer, create_marketing_strategy_agent,
    create_supply_chain_agent
)
from src.tasks.tasks import (
    create_analysis_task, create_optimization_task,
    create_automation_task, create_marketing_task,
    create_supply_chain_task
)
from feedback_loop import FeedbackLoop, MarketingStrategyAgent
from src.utils.sentiment_analysis import SentimentAnalyzer
from src.ml.forecaster import SalesForecaster
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()


def main():
    try:
        # Create mock data
        company_data = create_realistic_mock_data()

        print(company_data.head())
        print(company_data.describe())

        # Create outcome tracker
        tracker = OutcomeTracker(company_data)

        # Perform sentiment analysis
        analyzer = SentimentAnalyzer()
        feedback_data = pd.DataFrame({
            'Date': company_data['Date'],
            'Feedback': ["Sample feedback " + str(i) for i in range(len(company_data))]
        })
        analyzed_feedback = analyzer.analyze_feedback(feedback_data)

        try:
            analyzer.plot_sentiment_trend(analyzed_feedback)
            print("Sentiment analysis completed. Trend plot saved as 'static/sentiment_trend.png'")
        except Exception as e:
            print(f"Error saving sentiment trend plot: {str(e)}")

        # Perform sales forecasting
        forecaster = SalesForecaster()
        forecaster.train(company_data)
        future_dates = pd.date_range(start=company_data['Date'].max(), periods=30)
        forecasted_sales = forecaster.forecast(future_dates)

        try:
            forecaster.plot_forecast(company_data, future_dates, forecasted_sales)
            print("Sales forecast completed. Forecast plot saved as 'static/sales_forecast.png'")
        except Exception as e:
            print(f"Error saving sales forecast plot: {str(e)}")

        # Create agents
        data_analyst = create_data_analyst()
        process_optimizer = create_process_optimizer()
        automation_engineer = create_automation_engineer()
        marketing_strategist = create_marketing_strategy_agent()
        supply_chain_optimizer = create_supply_chain_agent()

        # Create tasks
        task1 = create_analysis_task(data_analyst, company_data)
        task2 = create_optimization_task(process_optimizer)
        task3 = create_automation_task(automation_engineer)
        task4 = create_marketing_task(marketing_strategist, company_data)
        task5 = create_supply_chain_task(supply_chain_optimizer, company_data)

        # Crew Setup
        crew = Crew(
            agents=[data_analyst, process_optimizer, automation_engineer, marketing_strategist, supply_chain_optimizer],
            tasks=[task1, task2, task3, task4, task5]
        )

        # Kickoff the crew
        result = crew.kickoff()
        print(result)

        # Implement feedback loop
        feedback_loop = FeedbackLoop(
            [data_analyst, process_optimizer, automation_engineer, marketing_strategist, supply_chain_optimizer],
            tracker)
        feedback_loop.update_agents()

        # Check if targets are met
        target_results = tracker.check_targets()
        print("Target Results:", target_results)

        return result, target_results, analyzed_feedback, forecasted_sales

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None, None, None


if __name__ == "__main__":
    main()