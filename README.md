# Project Development Crew

Welcome to the **Project Development Crew**, powered by [crewAI](https://crewai.com). This project is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

### Running OpenProject in Docker
This project uses **OpenProject** to manage project tasks and track progress. If you haven't already set up OpenProject in Docker, use the following command:

```bash
docker run -d --name openproject -p 8080:80 openproject/community:latest
```

Ensure that OpenProject is running at `http://localhost:8080` before proceeding.

### MLflow for Crew Execution Tracking
We use **MLflow** to keep track of Crew execution details. MLflow is configured to log execution data and track the progress of AI agents.

To start MLflow tracking, ensure you have it installed and running:

```bash
pip install mlflow
mlflow server --host 0.0.0.0 --port 5000
```

Make sure MLflow is running at `http://localhost:5000` and update the `.env` file accordingly:

```
MLFLOW_TRACKING_URI=http://localhost:5000
```

Ensure you have **Python >=3.10 <3.13** installed on your system.  
This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install UV:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

Alternatively, if you are using `pip` and `venv`, activate your virtual environment and run:
```bash
pip install -r requirements.txt
```

### **Setting Up Environment Variables**
Create a `.env` file in the root directory and add your API keys:
```
OPENPROJECT_API_URL=http://localhost:8080/api/v3
API_KEY=your-api-key-here
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT=CrewAI
```

### **Customizing Your AI Agents**
Modify the following files based on your needs:
- **Define Agents**: Modify `src/project_development/config/agents.yaml`
- **Define Tasks**: Modify `src/project_development/config/tasks.yaml`
- **Implement Logic & Tools**: Modify `src/project_development/crew.py`
- **Handle Inputs & Execution**: Modify `src/project_development/main.py`

## Running the Project

To kickstart your AI agents and begin task execution, run this from the **root** folder of your project:

```bash
crewai run
```

This command initializes the **Project Development Crew**, assembling the agents and assigning them tasks as defined in your configuration.

By default, this project will generate a `report.md` file containing the output of a research task.

## **Understanding Your Crew**

The **Project Development Crew** is composed of multiple AI agents, each with unique roles, goals, and tools.  
These agents collaborate on a series of tasks, leveraging their collective skills to achieve complex objectives.

- **Agents Configuration**: Defined in `config/agents.yaml`
- **Task Assignments**: Defined in `config/tasks.yaml`
- **Execution Flow**: Managed in `src/project_development/crew.py`

## **Repository & Contribution**
This repository is hosted at: **[GitHub Repo Link](your-repo-link-here)**  
Feel free to contribute, raise issues, or suggest improvements.

## **Support & Documentation**

For questions, support, or feedback:

- Visit the official [crewAI documentation](https://docs.crewai.com)
- Check out our [GitHub repository](your-repo-link-here)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of **crewAI** 🚀.

