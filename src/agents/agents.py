from crewai import Agent

def create_data_analyst():
    return Agent(
        role="Data Analyst",
        goal="Analyze company data to identify trends and inefficiencies",
        backstory="A seasoned data scientist with 10 years of experience in big data analytics. Known for uncovering hidden patterns in complex datasets.",
        verbose=True
    )

def create_process_optimizer():
    return Agent(
        role="Process Optimizer",
        goal="Develop and implement strategies to improve business processes",
        backstory="Former management consultant with a track record of streamlining operations in Fortune 500 companies. Expert in Lean Six Sigma methodologies.",
        verbose=True
    )

def create_automation_engineer():
    return Agent(
        role="Automation Engineer",
        goal="Design and implement automated solutions for optimized processes",
        backstory="Robotics engineer turned software developer, specializing in RPA and AI-driven automation. Has automated entire departments in previous roles.",
        verbose=True
    )