# AI Graph Workflow Engine

## Project Overview
This repository contains a modular Graph Engine built with Python, designed to orchestrate agent workflows. It is deployed as a FastAPI service that demonstrates a "Summarizing Agent" workflow.

WorkFlow Engine: This is a class that consist of Four basic elements. And this is used to create or define any automated Pipeline.
1. Nodes
2. Edges
3. Conditions
4. State

And there are functions to help with the workflow and to create workflow Where,

- `Nodes` : These are a autonomous blocks that are specialized for a certain task
- `Edges` : These are the the Direction and path from One node to another, Basically Defining 
        the pipeline.
- `State` : States is a term here that is given to define the current position of the process. 
        At what step the process is on.
- `Condition` : This is basically a check to control the quality or some condition before proceeding
            from one state to another

## Folder Structure
- `app/`: Contains the FastAPI application and API endpoints.
- `core/`: Contains the `GraphEngine(as graphengine.py)` logic and the `SummarizingAgent(as agent.py)` workflow definitions.
- `requirements.txt`: List of dependencies.

## How to Run

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Setup Virtual Environment
It is best practice to run this project in a virtual environment.

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
uvicorn app.main:app --reload
```

My Resume Link : https://drive.google.com/file/d/1CKxlobGNZO5twDOioXKZ_IlKpm4fKoTO/view?usp=drive_link
