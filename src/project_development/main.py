# import json
# import asyncio
# import aiohttp
# import base64
# from pydantic import BaseModel
# from crewai.flow import Flow, listen, start
# from project_development.crews.project_planning_crew.project_planning_crew import ProjectPlanning
# from project_development.crews.open_project_crew.open_project_crew import OpenProjectCrew
# import mlflow

# mlflow.crewai.autolog()

# # Optional: Set a tracking URI and an experiment name if you have a tracking server
# mlflow.set_tracking_uri("http://localhost:5000")
# mlflow.set_experiment("CrewAI")


# class Input(BaseModel):
#     client_requirements: str = "App to engage people in healthy communication. App should have points-based scoring features to provide tracking of app users."
#     project_plan: str = ""
#     project_title: str = ""
#     work_packages: list = []  # List of dicts with "name" and "tasks"


# class ProjectPlanningFlow(Flow[Input]):
#     OPENPROJECT_API_URL = "http://localhost:8080/api/v3"
#     API_KEY = "adc6afbdd42fd111184e462dd8edbbf3c25b10434d30ff928acd22dc13ea3506"

#     def get_headers(self):
#         """Returns the authentication headers using API key."""
#         credentials = f"apikey:{self.API_KEY}"
#         encoded_credentials = base64.b64encode(credentials.encode()).decode()
#         return {
#             "Authorization": f"Basic {encoded_credentials}",
#             "Content-Type": "application/json"
#         }

#     @start()
#     def client_input(self):
#         print("Client Requirement:", self.state.client_requirements)

#     @listen(client_input)
#     def generate_project_plan(self):
#         print("Commencing project planning")
#         result = (
#             ProjectPlanning()
#             .crew()
#             .kickoff(inputs={"client_requirements": self.state.client_requirements})
#         )

#         print("Project Plan Generated:", result.raw)
#         self.state.project_plan = result.raw

#     @listen(generate_project_plan)
#     def save_project_plan(self):
#         print("Saving project plan")
#         with open("project_plan.txt", "w") as f:
#             f.write(self.state.project_plan)

#     @listen(save_project_plan)
#     def open_project(self):
#         print("Creating project, work packages, and tasks")

#         result = (
#             OpenProjectCrew()
#             .crew()
#             .kickoff(inputs={"project_plan": self.state.project_plan})
#         )

#         # Ensure result.raw is a dictionary before accessing keys
#         if isinstance(result.raw, str):
#             try:
#                 result_data = json.loads(result.raw)  # Convert string to dictionary
#             except json.JSONDecodeError:
#                 print("❌ Error: OpenProjectCrew returned invalid JSON format.")
#                 return
#         else:
#             result_data = result.raw  # Already a dictionary

#         # Extract structured data from OpenProjectCrew result
#         self.state.project_title = result_data.get("project_title", "Untitled Project")
#         self.state.work_packages = result_data.get("work_packages", [])

#     @listen(open_project)
#     async def create_project_in_openproject(self):
#         print("🚀 Executing API requests to create project, work packages, and tasks")

#         headers = self.get_headers()

#         async with aiohttp.ClientSession(headers=headers) as session:
#             # Step 1: Create Project in OpenProject
#             project_payload = {"name": self.state.project_title, "description": self.state.project_plan}
#             async with session.post(f"{self.OPENPROJECT_API_URL}/projects", json=project_payload) as resp:
#                 project_response = await resp.json()
#                 print("🔍 Project API Response:", project_response)

#                 if resp.status != 201:
#                     print("❌ Failed to create project. API Response:", project_response)
#                     return  # Stop execution if project creation fails

#                 project_id = project_response.get("id")

#             print(f"✅ Project created with ID: {project_id}")

#             # Step 2: Create Work Packages (Updated API Request)
#             for wp in self.state.work_packages:
#                 wp_payload = {
#                     "subject": wp["name"],  
#                     "_links": {
#                         "type": {"href": "/api/v3/types/1"},  # Corrected type reference
#                         "project": {"href": f"/api/v3/projects/{project_id}"}
#                     }
#                 }

#                 async with session.post(f"{self.OPENPROJECT_API_URL}/work_packages", json=wp_payload) as resp:
#                     wp_response = await resp.json()
#                     print("🔍 Work Package API Response:", wp_response)

#                     if resp.status != 201:
#                         print(f"❌ Failed to create work package: {wp['name']}")
#                         continue  # Skip to the next work package

#                     work_package_id = wp_response.get("id")

#                 print(f"✅ Work Package created: {wp['name']} (ID: {work_package_id})")

#                 # Step 3: Add Tasks to Work Packages (Updated API Request)
#                 for task in wp["tasks"]:
#                     task_payload = {
#                         "subject": task,
#                         "_links": {
#                             "parent": {"href": f"/api/v3/work_packages/{work_package_id}"},
#                             "project": {"href": f"/api/v3/projects/{project_id}"}
#                         }
#                     }

#                     async with session.post(f"{self.OPENPROJECT_API_URL}/work_packages", json=task_payload) as resp:
#                         task_response = await resp.json()
#                         print("🔍 Task API Response:", task_response)

#                         if resp.status != 201:
#                             print(f"❌ Failed to create task: {task}")
#                             continue  # Skip to the next task

#                         task_id = task_response.get("id")

#                     print(f"✅ Task created: {task} (ID: {task_id}) under {wp['name']}") 


# def kickoff():
#     project_flow = ProjectPlanningFlow()
#     asyncio.run(project_flow.kickoff())  # Ensure async execution


# def plot():
#     project_flow = ProjectPlanningFlow()
#     project_flow.plot()


# if __name__ == "__main__":
#     kickoff()


import os
import json
import asyncio
import aiohttp
import base64
from dotenv import load_dotenv
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from project_development.crews.project_planning_crew.project_planning_crew import ProjectPlanning
from project_development.crews.open_project_crew.open_project_crew import OpenProjectCrew
import mlflow

# Load environment variables
load_dotenv()

# Fetch values from environment variables
OPENPROJECT_API_URL = os.getenv("OPENPROJECT_API_URL")
API_KEY = os.getenv("API_KEY")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
MLFLOW_EXPERIMENT = os.getenv("MLFLOW_EXPERIMENT")

# Configure MLflow
mlflow.crewai.autolog()
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT)


class Input(BaseModel):
    client_requirements: str = "App to engage people in healthy communication. App should have points-based scoring features to provide tracking of app users."
    project_plan: str = ""
    project_title: str = ""
    work_packages: list = []  # List of dicts with "name" and "tasks"


class ProjectPlanningFlow(Flow[Input]):
    def get_headers(self):
        """Returns the authentication headers using API key."""
        credentials = f"apikey:{API_KEY}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

    @start()
    def client_input(self):
        print("Client Requirement:", self.state.client_requirements)

    @listen(client_input)
    def generate_project_plan(self):
        print("Commencing project planning")
        result = (
            ProjectPlanning()
            .crew()
            .kickoff(inputs={"client_requirements": self.state.client_requirements})
        )

        print("Project Plan Generated:", result.raw)
        self.state.project_plan = result.raw

    @listen(generate_project_plan)
    def save_project_plan(self):
        print("Saving project plan")
        with open("project_plan.txt", "w") as f:
            f.write(self.state.project_plan)

    @listen(save_project_plan)
    def open_project(self):
        print("Creating project, work packages, and tasks")

        result = (
            OpenProjectCrew()
            .crew()
            .kickoff(inputs={"project_plan": self.state.project_plan})
        )

        if isinstance(result.raw, str):
            try:
                result_data = json.loads(result.raw)
            except json.JSONDecodeError:
                print("❌ Error: OpenProjectCrew returned invalid JSON format.")
                return
        else:
            result_data = result.raw

        self.state.project_title = result_data.get("project_title", "Untitled Project")
        self.state.work_packages = result_data.get("work_packages", [])

    @listen(open_project)
    async def create_project_in_openproject(self):
        print("🚀 Executing API requests to create project, work packages, and tasks")

        headers = self.get_headers()

        async with aiohttp.ClientSession(headers=headers) as session:
            # Step 1: Create Project in OpenProject
            project_payload = {"name": self.state.project_title, "description": self.state.project_plan}
            async with session.post(f"{OPENPROJECT_API_URL}/projects", json=project_payload) as resp:
                project_response = await resp.json()
                print("🔍 Project API Response:", project_response)

                if resp.status != 201:
                    print("❌ Failed to create project. API Response:", project_response)
                    return

                project_id = project_response.get("id")

            print(f"✅ Project created with ID: {project_id}")

            # Step 2: Create Work Packages
            for wp in self.state.work_packages:
                wp_payload = {
                    "subject": wp["name"],  
                    "_links": {
                        "type": {"href": "/api/v3/types/1"},
                        "project": {"href": f"/api/v3/projects/{project_id}"}
                    }
                }

                async with session.post(f"{OPENPROJECT_API_URL}/work_packages", json=wp_payload) as resp:
                    wp_response = await resp.json()
                    print("🔍 Work Package API Response:", wp_response)

                    if resp.status != 201:
                        print(f"❌ Failed to create work package: {wp['name']}")
                        continue

                    work_package_id = wp_response.get("id")

                print(f"✅ Work Package created: {wp['name']} (ID: {work_package_id})")

                # Step 3: Add Tasks to Work Packages
                for task in wp["tasks"]:
                    task_payload = {
                        "subject": task,
                        "_links": {
                            "parent": {"href": f"/api/v3/work_packages/{work_package_id}"},
                            "project": {"href": f"/api/v3/projects/{project_id}"}
                        }
                    }

                    async with session.post(f"{OPENPROJECT_API_URL}/work_packages", json=task_payload) as resp:
                        task_response = await resp.json()
                        print("🔍 Task API Response:", task_response)

                        if resp.status != 201:
                            print(f"❌ Failed to create task: {task}")
                            continue

                        task_id = task_response.get("id")

                    print(f"✅ Task created: {task} (ID: {task_id}) under {wp['name']}") 


def kickoff():
    project_flow = ProjectPlanningFlow()
    asyncio.run(project_flow.kickoff())


def plot():
    project_flow = ProjectPlanningFlow()
    project_flow.plot()


if __name__ == "__main__":
    kickoff()



