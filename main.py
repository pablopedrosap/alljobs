import os
from crewai import Crew, Task
from agents import ProjectManagerAgent, ArchitectAgent, DeveloperAgent, CodeReviewerAgent, DevOpsAgent, WebScrapingAgent
<<<<<<< HEAD
from tools import CodeGenerationTool, ArchitectureTrackingTool

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

class AgentManager:
    
=======
from tools import CodeGenerationTool

class AIDevelopmentSystem:
>>>>>>> origin/main
    def __init__(self):
        self.pm = ProjectManagerAgent()
        self.architect = ArchitectAgent()
        self.developer = DeveloperAgent()
        self.reviewer = CodeReviewerAgent()
        self.devops = DevOpsAgent()
        self.web_scraper = WebScrapingAgent()
<<<<<<< HEAD

    def get_agent(self, agent_type: str):
        return getattr(self, agent_type.lower(), None)

    def delegate_task(self, task_description: str, agent_type: str):
        agent = self.get_agent(agent_type)
        if agent:
            return agent.execute_task(task_description)
        else:
            return f"No agent found for type: {agent_type}"
        
class AIDevelopmentSystem:
    def __init__(self):
        self.agent_manager = AgentManager()
        self.code_gen = CodeGenerationTool()
        self.architecture_tool = ArchitectureTrackingTool()

    # In the AIDevelopmentSystem class
    def create_tasks(self, feature_description):
        planning_task = Task(
            description=f"Plan the implementation of the following feature: {feature_description}",
            agent=self.agent_manager.get_agent("pm"),
            expected_output="A detailed project plan including tasks and task allocation to each agent.",
            output_file="project_plan.txt"
        )

        design_task = Task(
            description="Design the system architecture for the planned feature",
            agent=self.agent_manager.get_agent("architect"),
=======
        self.code_gen = CodeGenerationTool()

    def create_tasks(self, feature_description):
        # Task 1: Planning
        planning_task = Task(
            description=f"Plan the implementation of the following feature: {feature_description}",
            agent=self.pm,
            expected_output="A detailed project plan including tasks, timelines, and resource allocation.",
            output_file="project_plan.txt"
        )

        # Task 2: Design System Architecture
        design_task = Task(
            description="Design the system architecture for the planned feature",
            agent=self.architect,
>>>>>>> origin/main
            expected_output="A comprehensive system architecture document",
            context=[planning_task],
            output_file="system_architecture.txt"
        )

<<<<<<< HEAD
        web_scraping_task = Task(
            description=f"Scrape the web for information relevant to implementing {feature_description}. Focus on official documentation and API references.",
            agent=self.agent_manager.get_agent("web_scraper"),
            expected_output="Relevant, concise data extracted from authoritative sources, without examples unless explicitly needed.",
=======
        # Task 3: Web Scraping for Information (if needed)
        web_scraping_task = Task(
            description="Scrape the web for necessary information related to the feature",
            agent=self.web_scraper,
            expected_output="Relevant data extracted from the web",
>>>>>>> origin/main
            context=[design_task],
            output_file="scraped_data.txt"
        )

<<<<<<< HEAD
        implement_task = Task(
            description=f"Implement the designed feature: {feature_description}",
            agent=self.agent_manager.get_agent("developer"),
            expected_output="Completed code implementation of the feature with appropriate file structure",
            context=[self.architecture_tool.run("get_structure")],  # Use .run() instead of ._run()
            output_file="implementation_report.txt"
        )

        review_task = Task(
            description="Review the implemented code and ensure it aligns with the system architecture",
            agent=self.agent_manager.get_agent("reviewer"),
            expected_output="Code review report with suggestions for improvements",
            context=[implement_task, design_task],
            output_file="code_review_report.txt"
        )

        deploy_task = Task(
            description="Prepare and execute the deployment of the new feature, considering the system architecture",
            agent=self.agent_manager.get_agent("devops"),
            expected_output="Deployment report including steps taken and any issues encountered",
            context=[review_task, design_task],
=======
        # Task 4: Implement the Feature
        implement_task = Task(
            description="Implement the designed feature, possibly using code generated based on web-scraped data",
            agent=self.developer,
            expected_output="Completed code implementation of the feature",
            context=[web_scraping_task],
            output_file="feature_implementation.py"
        )

        # Task 5: Code Review
        review_task = Task(
            description="Review the implemented code",
            agent=self.reviewer,
            expected_output="Code review report with suggestions for improvements",
            context=[implement_task],
            output_file="code_review_report.txt"
        )

        # Task 6: Deploy the Feature
        deploy_task = Task(
            description="Prepare and execute the deployment of the new feature",
            agent=self.devops,
            expected_output="Deployment report including steps taken and any issues encountered",
            context=[review_task],
>>>>>>> origin/main
            output_file="deployment_report.txt"
        )

        return [planning_task, design_task, web_scraping_task, implement_task, review_task, deploy_task]

    def run(self, feature_description):
        crew = Crew(
<<<<<<< HEAD
            agents=[
                self.agent_manager.pm,
                self.agent_manager.architect,
                self.agent_manager.developer,
                self.agent_manager.reviewer,
                self.agent_manager.devops,
                self.agent_manager.web_scraper
            ],
            tasks=self.create_tasks(feature_description)
        )
        result = crew.kickoff()
        updated_architecture = self.architecture_tool.run("get_structure")
        print("Updated Project Structure:")
        print(updated_architecture)

        return result
       
=======
            agents=[self.pm, self.architect, self.developer, self.reviewer, self.devops, self.web_scraper],
            tasks=self.create_tasks(feature_description)
        )
        result = crew.kickoff()
        return result
>>>>>>> origin/main

def main():
    ai_system = AIDevelopmentSystem()
    feature_description = "Implement a user authentication system with OAuth2 support and web-based interactions"
    result = ai_system.run(feature_description)
<<<<<<< HEAD
    print(result)

if __name__ == "__main__":
    main()



=======
    
    print("AI Development System Execution Results:")
    for task in result.tasks:
        print(f"\nTask: {task.description}")
        print(f"Output file: {task.output_file}")
        if os.path.exists(task.output_file):
            with open(task.output_file, 'r') as file:
                print(f"Content:\n{file.read()}")
        else:
            print("Output file not found.")

if __name__ == "__main__":
    main()
>>>>>>> origin/main
