from crewai import Task

def create_analysis_task(agent, data):
    return Task(
        description=f"Analyze the following company data to identify top 3 inefficiencies: {data.to_json()}",
        agent=agent,
        expected_output="A detailed report listing the top 3 inefficiencies identified in the company data, including supporting statistics and potential impact on the business."
    )