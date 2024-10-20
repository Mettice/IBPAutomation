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
        feedback_loop = FeedbackLoop([data_analyst, process_optimizer, automation_engineer, marketing_strategist, supply_chain_optimizer], tracker)
        feedback_loop.update_agents()

        # Check if targets are met
        target_results = tracker.check_targets()
        print("Target Results:", target_results)

        return result, target_results

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None

if __name__ == "__main__":
    main()