import os
from crewai import Crew, Task
from agents import ProjectManagerAgent, ArchitectAgent, DeveloperAgent, CodeReviewerAgent, DevOpsAgent, WebScrapingAgent
from tools import CodeGenerationTool

class AIDevelopmentSystem:
    def __init__(self):
        self.pm = ProjectManagerAgent()
        self.architect = ArchitectAgent()
        self.developer = DeveloperAgent()
        self.reviewer = CodeReviewerAgent()
        self.devops = DevOpsAgent()
        self.web_scraper = WebScrapingAgent()
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
            expected_output="A comprehensive system architecture document",
            context=[planning_task],
            output_file="system_architecture.txt"
        )

        # Task 3: Web Scraping for Information (if needed)
        web_scraping_task = Task(
            description="Scrape the web for necessary information related to the feature",
            agent=self.web_scraper,
            expected_output="Relevant data extracted from the web",
            context=[design_task],
            output_file="scraped_data.txt"
        )

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
            output_file="deployment_report.txt"
        )

        return [planning_task, design_task, web_scraping_task, implement_task, review_task, deploy_task]

    def run(self, feature_description):
        crew = Crew(
            agents=[self.pm, self.architect, self.developer, self.reviewer, self.devops, self.web_scraper],
            tasks=self.create_tasks(feature_description)
        )
        result = crew.kickoff()
        return result

def main():
    ai_system = AIDevelopmentSystem()
    feature_description = "Implement a user authentication system with OAuth2 support and web-based interactions"
    result = ai_system.run(feature_description)
    
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
