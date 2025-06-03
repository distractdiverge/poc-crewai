from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
)
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class PocCrewaiDevelopers():
    """PocCrewaiDevelopers crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            reasoning=True,
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def reviewer(self) -> Agent:
        """New fact-checking agent"""
        return Agent(
            config=self.agents_config['reviewer'], # type: ignore[index]
            reasoning=True,
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
            tools=[SerperDevTool(), WebsiteSearchTool()]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'] # type: ignore[index]
        )
    
    @task
    def verification_task(self) -> Task:
        """Runs after reporting_task to validate every citation & claim"""
        return Task(
            config=self.tasks_config['verification_task'], # type: ignore[index]
            tools=[SerperDevTool(), WebsiteSearchTool()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PocCrewaiDevelopers crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
