import os
from crewai import Crew, Task, Process
from langchain_openai import ChatOpenAI
from agents import AgentManager
from tools import FileOperationTool, TerminalTool, DocumentationExtractionTool, set_architecture
import subprocess
import json

class AIDevelopmentSystem:
    def __init__(self):
        self.agent_manager = AgentManager()
        self.file_operation_tool = FileOperationTool()
        self.manager_llm = ChatOpenAI(model="gpt-4o-mini")

    def classify_task(self, feature_description):
        classification_task = Task(
            description=f"Classify the automation task and identify required specialized agents: {feature_description}",
            agent=self.agent_manager.classifier
        )
        classification_crew = Crew(
            agents=[self.agent_manager.classifier],
            tasks=[classification_task],
            process=Process.sequential
        )
        return classification_crew.kickoff()
    
    def generate_json_plan(self, feature_description):
        # Use an LLM to generate a structured JSON plan
        plan_task = Task(
            description=f"Generate a detailed JSON plan for: {feature_description}. Max 10 super specific steps. no timeline just actionable steps that can be implemented in code.",
            agent=self.agent_manager.planner,
            output_format="JSON"
        )
        plan_crew = Crew(
            agents=[self.agent_manager.planner],
            tasks=[plan_task],
            process=Process.sequential
        )
        return json.loads(plan_crew.kickoff())

    def create_architect_task(self, json_plan):
        return Task(
            description=f"Design the project structure based on this plan: {json_plan}",
            agent=self.agent_manager.architect,
            output_format="JSON",
            expected_output="""**No folders within folders and keep it really simple**. just output the structure...  example format-> {
                "project": "my_data_analysis_project",
                "structure": {
                    "data": ["data_file_1.csv", "data_file_2.xlsx"],
                    "tests": ["xx.py", "xx.py"],
                    ["main.py", "whatever.py"],
                }
            }"""
        )
    def identify_relevant_files(self, step, project_structure):
        # Logic to identify which files are relevant for the current step
        pass

    def execute_step(self, step, relevant_files, project_structure, json_plan):
        for file in relevant_files:
            file_content = self.file_operation_tool.read_file(file)
            context = self.context_extraction_tool.extract_context(file_content)
            task_type = self.classify_task(json_plan)
            specialized_agent = task_type['required_agent']
            
            while True:
                dev_task = Task(
                    description=f"Implement {step} for file {file}. If you need any clarification or additional information, use the HumanInputTool.",
                    agent=specialized_agent,
                    context=context,
                    expected_output=f""
                )
                dev_crew = Crew(agents=[specialized_agent], tasks=[dev_task])
                implementation = dev_crew.kickoff()
                
                review_task = Task(
                    description=f"Review implementation of {step} for file {file}",
                    agent=self.agent_manager.reviewer,
                    context=context,
                    expected_output=f""
                )
                review_crew = Crew(agents=[self.agent_manager.reviewer], tasks=[review_task])
                review = review_crew.kickoff()
                
                if review['status'] == 'complete':
                    self.file_operation_tool.write_file(file, implementation)
                    break
                
                else:
                    context += f"\nReview feedback: {review['feedback']}"

    def run(self, feature_description):
        json_plan = self.generate_json_plan(feature_description)
        
        architect_task = self.create_architect_task(json_plan)
        architect_crew = Crew(agents=[self.agent_manager.architect], tasks=[architect_task])
        project_structure = architect_crew.kickoff()
        
        for step in json_plan['steps']:
            relevant_files = self.identify_relevant_files(step, project_structure)
            self.execute_step(step, relevant_files, project_structure, json_plan)
        

def main():
    ai_system = AIDevelopmentSystem()
    feature_description = "This project automates core aspects of rental management for platforms like Airbnb and Booking.com, including calendar synchronization, dynamic pricing, guest communication, and financial reporting."
    project_name = ""

    result = ai_system.run(feature_description, project_name)
    print(result)

if __name__ == "__main__":
    main()



# specifically codes automation scripts, not general software.
# classifier llm for pipeline and direct to specific dev agent with specific doscs.
# human in the loop for needed data, doubts, or logins
# 
# input parsing (json with empty values and steps) - automation script generation (with llms) - testing - development and scheduling.

# Node.js, react, PyTorch, Scikit-learn, unity, Google Cloud APIs, Docker, openai and crewai frameworks 
# the developer is not one, there is a developer per function expert in the above frameworks.


