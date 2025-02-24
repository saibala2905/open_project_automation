from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from typing import List, Dict

class WorkPackage(BaseModel):
    name: str = Field(..., title="Work Package Name", min_length=1)
    tasks: List[str] = Field(default=[], title="Tasks", description="List of task names")

class ProjectData(BaseModel):
    project_title: str = Field(..., title="Project Title", min_length=1)
    work_packages: List[WorkPackage] = Field(default=[], title="Work Packages", description="List of work packages with tasks")


@CrewBase
class OpenProjectCrew:
    """Open Project Crew"""
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def admin_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["admin_agent"],
        )

    @task
    def admin_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config["admin_agent_task"],
            output_pydantic=ProjectData
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Open Project Crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
