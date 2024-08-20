import os
from crewai import Crew, Task, Process
from langchain_openai import ChatOpenAI
from agents import AgentManager
from tools import FileOperationTool, TerminalTool, HTMLExtractionTool, DocumentationExtractionTool, set_architecture
import subprocess
import json

class AIDevelopmentSystem:
    def __init__(self):
        self.agent_manager = AgentManager()
        self.file_operation_tool = FileOperationTool()
        self.manager_llm = ChatOpenAI(model="gpt-4o-mini")

    def create_architect_task(self, task_description):
        return Task(
            description=f"Design the project structure for: {task_description}.",
            agent=self.agent_manager.architect,
            output_format="JSON",
            expected_output="""Only JSON structure(nothing before or after) defining the project directories and files. ***this is just an Example to know the exact format, no comments or explanations. No folders within folders and all files in lists.:
                            
            {
                "project": "my_data_analysis_project",
                {"structure": {
                    "data": ["data_file_1.csv", "data_file_2.xlsx"]},{
                    "notebooks": ["data_exploration.ipynb", "model_training.ipynb"]},{
                    "scripts": ["preprocess_data.py", "train_model.py", "evaluate_model.py"]}
                }
            } 
            """
        )

    def create_developer_task(self, task_description, project_structure, project_name):
        return Task(
            description=f"Develop the feature: {task_description}. this is the project tree: {project_structure}, with project name: {project_name}",
            agent=self.agent_manager.developer,
            expected_output="Full Software code implementing the feature using complete code and open source libraries if necessary."
        )

    def create_reviewer_task(self, task_description, project_structure, project_name):
        return Task(
            description=f"Review the code for: {task_description}.  this is the project tree: {project_structure}, with project name: {project_name}",
            agent=self.agent_manager.reviewer,
            expected_output="A brief code review report."
        )

    def create_devops_task(self, task_description):
        return Task(
            description=f"Prepare the deployment plan for: {task_description}",
            agent=self.agent_manager.devops,
            expected_output="A straightforward deployment plan."
        )

    def run(self, feature_description):
        # Architect stage
        architect_task = self.create_architect_task(feature_description)
        architect_crew = Crew(
            agents=[self.agent_manager.architect],
            tasks=[architect_task],
            process=Process.sequential,
            memory=True,
        )
        project_structure = str(architect_crew.kickoff())
        project_name = set_architecture(json.loads(project_structure))

        # Developer stage
        while True:
            developer_task = self.create_developer_task(feature_description, project_structure, project_name)
            developer_crew = Crew(
                agents=[self.agent_manager.developer],
                tasks=[developer_task],
                process=Process.sequential,
                memory=True,
            )
            code_output = developer_crew.kickoff()

            # Reviewer stage
            reviewer_task = self.create_reviewer_task(feature_description, project_structure, project_name)
            reviewer_crew = Crew(
                agents=[self.agent_manager.reviewer],
                tasks=[reviewer_task],
                process=Process.sequential,
                memory=True,
            )
            review_output = str(reviewer_crew.kickoff())
            if 'not_finished' not in review_output.lower():
                break

        # DevOps stage
        devops_task = self.create_devops_task(feature_description)
        devops_crew = Crew(
            agents=[self.agent_manager.devops],
            tasks=[devops_task],
            process=Process.sequential,
            memory=True,
        )
        deployment_plan = devops_crew.kickoff()

        return {
            "project_structure": project_structure,
            "code_output": code_output,
            "review_output": review_output,
            "deployment_plan": deployment_plan
        }

def main():
    ai_system = AIDevelopmentSystem()
    feature_description = "create a website for photography in madrid, eleina scarced."
    result = ai_system.run(feature_description)
    print(result)

if __name__ == "__main__":
    main()



#single crews-> architect, loop coder(tools: docu&api searcher, webscraping for automation) + reviewer(tools: terminal, vision), git, devops... .. 