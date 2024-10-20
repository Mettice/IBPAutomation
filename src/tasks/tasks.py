from crewai import Task

def create_analysis_task(agent, data):
    return Task(
        description=f"Analyze the following company data to identify top 3 inefficiencies: {data.to_json()}",
        agent=agent
    )

def create_optimization_task(agent):
    return Task(
        description="Develop a process improvement plan addressing the identified inefficiencies",
        agent=agent
    )

def create_automation_task(agent):
    return Task(
        description="Create an automation script to implement the top priority process improvement",
        agent=agent
    )