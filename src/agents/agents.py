from crewai import Agent
from src.utils.sentiment_analysis import sentiment_analysis_tool

def create_data_analyst():
    return Agent(
        role="Data Analyst",
        goal="Analyze company data to identify trends and inefficiencies",
        backstory="A seasoned data scientist with 10 years of experience in big data analytics. Known for uncovering hidden patterns in complex datasets.",
        allow_delegation=False
    )

def create_process_optimizer():
    return Agent(
        role="Process Optimizer",
        goal="Develop and implement strategies to improve business processes",
        backstory="Former management consultant with a track record of streamlining operations in Fortune 500 companies. Expert in Lean Six Sigma methodologies.",
        allow_delegation=False
    )

def create_automation_engineer():
    return Agent(
        role="Automation Engineer",
        goal="Design and implement automated solutions for optimized processes",
        backstory="Robotics engineer turned software developer, specializing in RPA and AI-driven automation. Has automated entire departments in previous roles.",
        allow_delegation=False
    )

def create_marketing_strategy_agent():
    return Agent(
        role="Marketing Strategist",
        goal="Develop data-driven marketing strategies to improve sales and customer satisfaction",
        backstory="Experienced digital marketing expert with a track record of successful campaigns across various industries.",
        allow_delegation=False,
        tools=[sentiment_analysis_tool]
    )

def create_supply_chain_agent():
    return Agent(
        role="Supply Chain Optimizer",
        goal="Optimize the supply chain to reduce costs and improve efficiency",
        backstory="Expert in supply chain management with experience in implementing just-in-time inventory systems and reducing waste.",
        allow_delegation=False
    )