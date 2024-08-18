import os
from crewai import Crew, Task, Process
from langchain_openai import ChatOpenAI
from agents import AgentManager
from tools import ArchitectureTrackingTool, FileOperationTool, WebScrapingTool

class AIDevelopmentSystem:
    def __init__(self):
        self.agent_manager = AgentManager()
        self.architecture_tool = ArchitectureTrackingTool()
        self.file_operation_tool = FileOperationTool()
        self.web_scraping_tool = WebScrapingTool()
        self.manager_llm = ChatOpenAI(model="gpt-4o-mini")

    def create_initial_task(self, feature_description):
        return Task(
            description=f"Plan simply and outline the project for: {feature_description}",
            agent=self.agent_manager.pm,
            expected_output="A basic project plan with essential tasks."
        )

    def create_architect_task(self, task_description):
        return Task(
            description=f"Design the project structure for: {task_description}.",
            agent=self.agent_manager.architect,
            execute=self.execute_architect_task,
            expected_output="""much simplified version with this example format ---> project_structure = {
                "src": {
                    "components": ["header.js", "footer.js"],
                    "pages": ["home.js", "about.js"],
                    "styles": ["main.css", "theme.css"],
                    "utils": ["helpers.py", "validators.py"]
                },
                "tests": {
                    "unit": ["test_helpers.py", "test_validators.py"],
                    "integration": ["test_integration.py"]
                },
                "assets": {
                    "images": ["logo.png", "banner.jpg"],
                    "fonts": ["custom.ttf"]
                },
                "docs": ["README.md", "CONTRIBUTING.md"],
                "scripts": {
                    "deployment": ["deploy.sh"],
                    "setup": ["setup.sh"]
                }
            }."""   
        )

    def execute_architect_task(self, task_description):
        project_structure = self.manager_llm.predict(f"""
        Create a simple and flexible project structure in JSON format for:
        {task_description}.
        The structure should include file paths that can be used directly in subsequent tasks.
        """)
        
        self.architecture_tool._run("set_structure", {"structure": project_structure})
        
        return project_structure

    def create_developer_task(self, task_description):
        return Task(
            description=f"Develop the feature: {task_description}",
            agent=self.agent_manager.developer,
            execute=self.execute_developer_task,
            expected_output="Python code implementing the feature."
        )

    def execute_developer_task(self, task_description):
        # Assuming task_description contains relevant file name or task description
        file_path_prompt = self.architecture_tool._run("get_file_path", {"task_description": task_description})
        implementation = self.manager_llm.predict(f"""
        Write the code for: {task_description}
        The file should be saved at: {file_path_prompt}.
        Ensure the code is well-documented.
        """)
        
        self.file_operation_tool._run("write", {"file_path": file_path_prompt, "content": implementation})
        
        return f"Code written to {file_path_prompt}"

    def create_reviewer_task(self, task_description):
        return Task(
            description=f"Review the code for: {task_description}",
            agent=self.agent_manager.reviewer,
            execute=self.execute_reviewer_task,
            expected_output="A brief code review report."
        )

    def execute_reviewer_task(self, task_description):
        review = self.manager_llm.predict(f"""
        Review the code for: {task_description}
        Provide feedback on quality and best practices.
        """)
        return review

    def create_devops_task(self, task_description):
        return Task(
            description=f"Prepare the deployment plan for: {task_description}",
            agent=self.agent_manager.devops,
            execute=self.execute_devops_task,
            expected_output="A straightforward deployment plan."
        )

    def execute_devops_task(self, task_description):
        plan = self.manager_llm.predict(f"""
        Create a simple deployment plan for: {task_description}
        Include setup, deployment commands, and rollback steps.
        """)
        return plan

    def create_web_scraping_task(self, task_description):
        return Task(
            description=f"Plan web scraping for: {task_description}",
            agent=self.agent_manager.web_scraper,
            execute=self.execute_web_scraping_task,
            expected_output="A basic web scraping plan."
        )

    def execute_web_scraping_task(self, task_description):
        scraping_plan = self.manager_llm.predict(f"""
        Create a web scraping plan for: {task_description}
        Include target sites, data points, and storage method.
        """)
        return scraping_plan

    def run(self, feature_description):
        tasks = [
            self.create_initial_task(feature_description),
            self.create_architect_task(feature_description),
            self.create_developer_task(feature_description),
            self.create_reviewer_task(feature_description),
            self.create_devops_task(feature_description),
            self.create_web_scraping_task(feature_description)
        ]
        crew = Crew(
            agents=[
                self.agent_manager.pm,
                self.agent_manager.architect,
                self.agent_manager.developer,
                self.agent_manager.reviewer,
                self.agent_manager.devops,
                self.agent_manager.web_scraper
            ],
            tasks=tasks,
            process=Process.hierarchical,
            manager_llm=self.manager_llm,
            memory=True,
            manager_agent=None,
            planning=True,
        )
        result = crew.kickoff()
        return result

def main():
    ai_system = AIDevelopmentSystem()
    feature_description = "Create a website for gsnus, a natural no nicotine snus."
    result = ai_system.run(feature_description)
    print(result)

if __name__ == "__main__":
    main()
