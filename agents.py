from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import FileOperationTool, ArchitectureTrackingTool, WebScrapingTool

llm4o = ChatOpenAI(model="gpt-4o-mini")

class AgentManager():
    def __init__(self):
        self.pm = ProjectManagerAgent()
        self.architect = ArchitectAgent()
        self.developer = DeveloperAgent()
        self.reviewer = CodeReviewerAgent()
        self.devops = DevOpsAgent()
        self.web_scraper = WebScrapingAgent()

class ProjectManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Project Manager',
            goal='Plan, delegate, and manage development tasks',
            backstory="Experienced PM creating and overseeing project plans for software projects.",
            verbose=True,
            llm=llm4o
        )

class ArchitectAgent(Agent):
    def __init__(self):
        super().__init__(
            role='System Architect',
            goal='Design simple and flexible architectures, you focus on making as few files as possible to be simplistic.',
            backstory="Architect creating basic structures for software projects.",
            tools=[ArchitectureTrackingTool()],
            verbose=True,
            llm=llm4o
        )

    def set_project_structure(self, project_name, structure):
        """
        Sets the project structure within the 'structure' directory.
        """
        structure_root = f"structures/{project_name}"
        self.tools[0]._run("set_structure", {"project": structure_root, "structure": structure})

class DeveloperAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Software Developer',
            goal='Implement features with clean, adaptable code',
            backstory="Developer writing efficient code within defined structures.",
            tools=[FileOperationTool(), ArchitectureTrackingTool()],
            verbose=True,
            llm=llm4o
        )

class CodeReviewerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Code Reviewer',
            goal='Review code for quality and best practices',
            backstory="Reviewer ensuring code meets quality standards.",
            tools=[FileOperationTool()],
            verbose=True,
            llm=llm4o
        )

class DevOpsAgent(Agent):
    def __init__(self):
        super().__init__(
            role='DevOps Engineer',
            goal='Prepare and manage deployment processes',
            backstory="DevOps engineer ensuring smooth deployments.",
            tools=[],
            verbose=True,
            llm=llm4o
        )

class WebScrapingAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Web Scraper',
            goal='Extract relevant web data',
            backstory="Expert in extracting and storing web data.",
            tools=[WebScrapingTool()],
            verbose=True,
            llm=llm4o
        )
