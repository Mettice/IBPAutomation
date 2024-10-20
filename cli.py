import click
from crewai import Crew
from src.utils.data_utils import create_realistic_mock_data
from src.agents.agents import (
    create_data_analyst, create_process_optimizer,
    create_automation_engineer, create_marketing_strategy_agent
)
from src.tasks.tasks import (
    create_analysis_task, create_optimization_task,
    create_automation_task, create_marketing_task
)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--start-date', default='2023-01-01', help='Start date for data simulation')
@click.option('--end-date', default='2023-12-31', help='End date for data simulation')
def run_ibpa(start_date, end_date):
    """Run the full IBPA process"""
    click.echo("Starting IBPA process...")

    # Create mock data
    company_data = create_realistic_mock_data(start_date, end_date)
    click.echo(f"Created mock data from {start_date} to {end_date}")

    # Create agents
    data_analyst = create_data_analyst()
    process_optimizer = create_process_optimizer()
    automation_engineer = create_automation_engineer()
    marketing_strategist = create_marketing_strategy_agent()

    # Create tasks
    tasks = [
        create_analysis_task(data_analyst, company_data),
        create_optimization_task(process_optimizer),
        create_automation_task(automation_engineer),
        create_marketing_task(marketing_strategist)
    ]

    # Crew Setup
    crew = Crew(
        agents=[data_analyst, process_optimizer, automation_engineer, marketing_strategist],
        tasks=tasks
    )

    # Kickoff the crew
    result = crew.kickoff()

    # Save results
    with open('ibpa_results.txt', 'w') as f:
        f.write(result)

    click.echo("IBPA process completed. Results saved to ibpa_results.txt")


@cli.command()
def view_results():
    """View the latest IBPA results"""
    try:
        with open('ibpa_results.txt', 'r') as f:
            click.echo(f.read())
    except FileNotFoundError:
        click.echo("No results found. Run the IBPA process first.")


if __name__ == '__main__':
    cli()