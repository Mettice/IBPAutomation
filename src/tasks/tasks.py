
from crewai import Task

def create_analysis_task(agent, data):
    return Task(
        description=f"Analyze the following company data to identify top 3 inefficiencies: {data.to_json()}",
        agent=agent,
        expected_output="A detailed report listing the top 3 inefficiencies identified in the company data, including supporting statistics and potential impact on the business."
    )

def create_optimization_task(agent):
    return Task(
        description="Develop a process improvement plan addressing the identified inefficiencies",
        agent=agent,
        expected_output="A comprehensive process improvement plan that addresses the top 3 inefficiencies, including specific action items, timelines, and expected outcomes."
    )

def create_automation_task(agent):
    return Task(
        description="Create an automation script to implement the top priority process improvement",
        agent=agent,
        expected_output="A detailed automation script or pseudocode that outlines the steps to implement the highest priority process improvement, including necessary tools and potential challenges."
    )

def create_marketing_task(agent, data):
    return Task(
        description=f"Analyze the sales and customer satisfaction data to develop a targeted marketing strategy: {data.to_json()}",
        agent=agent,
        expected_output="A comprehensive marketing strategy including target audience analysis, channel recommendations, and campaign ideas tied to the sales and satisfaction data."
    )

def create_supply_chain_task(agent, data):
    return Task(
        description=f"Analyze the current supply chain data and propose optimization strategies: {data.to_json()}",
        agent=agent,
        expected_output="A detailed plan for supply chain optimization, including inventory management strategies, supplier relationship improvements, and logistics enhancements."
    )