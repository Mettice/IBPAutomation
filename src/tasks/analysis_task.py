echo from crewai import Task

def create_analysis_task(agent, data):
    return Task(
        description=f"Analyze the company data and provide insights. Raw data: {data.to_json()}",
        agent=agent
    )
