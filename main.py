import os
from crewai import Crew, Task
from agents import ProjectManagerAgent, ArchitectAgent, DeveloperAgent, CodeReviewerAgent, DevOpsAgent, WebScrapingAgent
from tools import CodeGenerationTool, ArchitectureTrackingTool

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

class AgentManager:
    def __init__(self):
        self.pm = ProjectManagerAgent()
        self.architect = ArchitectAgent()
        self.developer = DeveloperAgent()
        self.reviewer = CodeReviewerAgent()
        self.devops = DevOpsAgent()
        self.web_scraper = WebScrapingAgent()

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
            expected_output="A comprehensive system architecture document",
            context=[planning_task],
            output_file="system_architecture.txt"
        )

        web_scraping_task = Task(
            description=f"Scrape the web for information relevant to implementing {feature_description}. Focus on official documentation and API references.",
            agent=self.agent_manager.get_agent("web_scraper"),
            expected_output="Relevant, concise data extracted from authoritative sources, without examples unless explicitly needed.",
            context=[design_task],
            output_file="scraped_data.txt"
        )

        architecture_structure = self.architecture_tool.run("get_structure")

        implement_task = Task(
            description=f"Implement the designed feature: {feature_description}. The current architecture structure is as follows:\n{architecture_structure}",
            agent=self.agent_manager.get_agent("developer"),
            expected_output="Completed code implementation of the feature with appropriate file structure",
            context=[],  # No additional context
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
            output_file="deployment_report.txt"
        )

        return [planning_task, design_task, web_scraping_task, implement_task, review_task, deploy_task]

    def run(self, feature_description):
        crew = Crew(
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
       

def main():
    ai_system = AIDevelopmentSystem()
    feature_description = "create a website to sell gsnus, a snus with no nicotine with natural herbs "
    result = ai_system.run(feature_description)
    print(result)

if __name__ == "__main__":
    main()



