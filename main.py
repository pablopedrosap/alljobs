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
            expected_output="""No folders within folders and all files in lists. just output the structure...  example format-> {
                "project": "my_data_analysis_project",
                "structure": {
                    "data": ["data_file_1.csv", "data_file_2.xlsx"],
                    "notebooks": ["data_exploration.ipynb", "model_training.ipynb"],
                    "scripts": ["preprocess_data.py", "train_model.py", "evaluate_model.py"],
                    ["main.py", whatever.py],
                }
            }"""
        )

    def create_developer_task(self, task_description, project_structure, project_name, feedback=''):
        feedback_text = f"{feedback}. " if feedback else ''
        return Task(
            description=f"{feedback_text} Develop the feature: {task_description}. This is the project tree: {project_structure}, starting file path with project name: {project_name}, and given the tree ensure the file path when calling the tool is correct.",
            agent=self.agent_manager.developer,
            expected_output=f"Full Software code implementing the feature using complete code and open source libraries if necessary, complete all code files within the tree structure: {project_structure}."
        )

    def create_reviewer_task(self, task_description, project_structure, project_name):
        return Task(
            description=f"Review the code for: {task_description}, read all code files within the tree structure. This is the project tree: {project_structure}, starting file path with project name: {project_name}, and given the tree ensure the file path when calling the tool is correct.",
            agent=self.agent_manager.reviewer,
            expected_output=f"**Include 'Not finished' in the review if developer has still job to do.** Provide a detailed code review report and proper feedback that will go to developer to improve the code, just focus on efficacy and extreme human like detail as steve jobs would, but do not overcomplicate. **for file paths:{project_structure}.**"
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
        feedback=''
        while True:
            developer_task = self.create_developer_task(feature_description, project_structure, project_name, feedback)
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
            feedback = f'This is the feedback from the reviewer from the code you have done: ***{review_output}***.'
            if 'not finished' not in review_output.lower():
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
    feature_description = "Crea un pagina web de 1 página solo en la que haya un cuadrado flotante de color verde que gire a medida que bajas la página."
    result = ai_system.run(feature_description)
    print(result)

if __name__ == "__main__":
    main()



#single crews-> architect, loop coder(tools: docu&api searcher, webscraping for automation) + reviewer(tools: terminal, vision), git, devops... .. 