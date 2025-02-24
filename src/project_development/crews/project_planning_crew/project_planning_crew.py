from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from crewai.tools import tool
import requests

# class ProjectPlan(BaseModel):
#     title: str
#     components: list[str]
#     tasks: list[str]
#     developers: list[str]

@CrewBase
class ProjectPlanning:
    """Project Planning Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    # @tool("create_project")
    # def create_project(project_title: str) -> str:
    #     """Tool description for clarity."""
        
    #     url = "http://localhost:8080/api/v3/projects"

    #     payload = {"name": project_title}
    #     headers = {
    #         'Authorization': 'Basic YXBpa2V5OmFkYzZhZmJkZDQyZmQxMTExODRlNDYyZGQ4ZWRiYmYzYzI1YjEwNDM0ZDMwZmY5MjhhY2QyMmRjMTNlYTM1MDY=',
    #         'Content-Type': 'application/json'
    #     }

    #     response = requests.post(url, headers=headers)

    #     print(response.text)
    #     return response.text
        
    @agent
    def ui_ux_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["ui_ux_designer"],
        )
    
    @agent
    def react_developer(self) -> Agent:
        return Agent(
            config = self.agents_config["react_developer"]
        )
    
    @agent
    def mongodb_expert(self) -> Agent:
        return Agent(
            config = self.agents_config["mongodb_expert"]
        )
        
    @agent
    def nodejs_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["nodejs_developer"]
        )

    @agent
    def project_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["project_manager"],
        )
        

        
    @task
    def ui_ux_designer_task(self) -> Task:
        return Task(
            config=self.tasks_config["ui_ux_designer_task"],
        )
        
    @task
    def react_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config["react_developer_task"],
        )
        
    @task
    def mongodb_expert_task(self) -> Task:
        return Task(
            config=self.tasks_config["mongodb_expert_task"],
        )
    
    @task
    def nodejs_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config["nodejs_developer_task"],
        )
    
    @task
    def project_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["project_planning_task"],
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the Project Planning Crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks,  
            # manager_agent=self.agents_config["project_manager"],
            process=Process.sequential,
            verbose=True,
        )
