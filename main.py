from crewai import Crew, Process
from src.utils.data_utils import create_mock_data
from src.agents.agents import create_data_analyst, create_process_optimizer, create_automation_engineer
from src.tasks.tasks import create_analysis_task, create_optimization_task, create_automation_task

def main():
    # Create mock data
    company_data = create_mock_data()

    # Create agents
    data_analyst = create_data_analyst()
    process_optimizer = create_process_optimizer()
    automation_engineer = create_automation_engineer()

    # Create tasks
    task1 = create_analysis_task(data_analyst, company_data)
    task2 = create_optimization_task(process_optimizer)
    task3 = create_automation_task(automation_engineer)

    # Crew Setup
    ibpa_crew = Crew(
        agents=[data_analyst, process_optimizer, automation_engineer],
        tasks=[task1, task2, task3],
        verbose=2,
        process=Process.sequential
    )

    # Kickoff the crew
    result = ibpa_crew.kickoff()
    print(result)

if __name__ == "__main__":
    main()