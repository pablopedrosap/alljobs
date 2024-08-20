import os
from crewai import Crew, Task, Process
from langchain_openai import ChatOpenAI
from agents import AgentManager
from tools import ArchitectureTrackingTool, FileOperationTool, WebScrapingTool, TerminalTool
import subprocess

class AIDevelopmentSystem:
    def __init__(self):
        self.agent_manager = AgentManager()
        self.architecture_tool = ArchitectureTrackingTool()
        self.file_operation_tool = FileOperationTool()
        self.web_scraping_tool = WebScrapingTool()
        self.manager_llm = ChatOpenAI(model="gpt-4o-mini")

    def create_architect_task(self, task_description):
        return Task(
            description=f"Design the project structure for: {task_description}.",
            agent=self.agent_manager.architect,
            expected_output="""A JSON structure defining the project directories and files. ***this is just an Example to know the format:
                            
            {
              "operation": "set_structure",
              "content": {
                "project": "xxxx",
                "structure": {
                  "directories": {
                    "images": {},
                    "assets": {},
                    "css": {},
                    "js": {}
                  },
                  "files": ["index.html", "styles.css", "script.js"]
                }
              }
            }   
            """
        )

    def create_developer_task(self, task_description):
        result = subprocess.run('tree structures', shell=True, check=True, text=True, capture_output=True)
        result = result.stdout
        return Task(
            description=f"Develop the feature: {task_description}. this is the project tree: {result}",
            agent=self.agent_manager.developer,
            expected_output="Software code implementing the feature."
        )

    def create_reviewer_task(self, task_description):
        result = subprocess.run('tree structures', shell=True, check=True, text=True, capture_output=True)
        result = result.stdout
        return Task(
            description=f"Review the code for: {task_description}.  this is the project tree: {result}",
            agent=self.agent_manager.reviewer,
            expected_output="A brief code review report."
        )

    def create_devops_task(self, task_description):
        return Task(
            description=f"Prepare the deployment plan for: {task_description}",
            agent=self.agent_manager.devops,
            expected_output="A straightforward deployment plan."
        )

    def create_web_scraping_task(self, task_description):
        return Task(
            description=f"Plan web scraping for: {task_description}",
            agent=self.agent_manager.web_scraper,
            expected_output="A basic web scraping plan."
        )

    def run(self, feature_description):
        tasks = [
            self.create_architect_task(feature_description),
            self.create_developer_task(feature_description),
            self.create_reviewer_task(feature_description),
            self.create_devops_task(feature_description),
            self.create_web_scraping_task(feature_description)
        ]
        crew = Crew(
            agents=[
                self.agent_manager.architect,
                self.agent_manager.developer,
                self.agent_manager.reviewer,
                self.agent_manager.devops,
                self.agent_manager.web_scraper
            ],
            tasks=tasks,
            process=Process.hierarchical,
            memory=True,
            manager_agent=self.agent_manager.pm,
            planning=True,
        )
        result = crew.kickoff()
        return result

def main():
    ai_system = AIDevelopmentSystem()
    feature_description = "search a good rag video and install it in mp4"
    result = ai_system.run(feature_description)
    print(result)

if __name__ == "__main__":
    main()




#single crews-> architect, loop coder(tools: docu&api searcher, webscraping for automation) + reviewer(tools: terminal, vision), git, crew devops... feedback live then improves architect and loop.. 