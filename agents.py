from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import FileOperationTool, TerminalTool
from crewai_tools import CodeDocsSearchTool, CodeInterpreterTool, HumanInputTool

llm4o = ChatOpenAI(model="gpt-4o-mini")

class AgentManager():
    def __init__(self):
        self.pm = ProjectManagerAgent()
        self.architect = ArchitectAgent()
        self.classifier = ClassifierAgent()
        self.web_automation = WebAutomationAgent()
        self.api_integration = APIIntegrationAgent()
        self.reviewer = CodeReviewerAgent()
        self.devops = DevOpsAgent()

class ProjectManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Project manager and ai prompt creator",
            goal="Provide input for the workflow of agents given the main idea of the user prompt",
            backstory="You're an experienced project manager, skilled in defining a prompt short and specific so the team can fulfill the user request",
            allow_delegation=True,
            verbose=True,
            llm=llm4o
        )

class CrewAIAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Expert in ai agents in the crewai framework",
            goal="",
            backstory="",
            allow_delegation=True,
            verbose=True,
            llm=llm4o
        )
        
class CrewAIAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Expert in ai agents in the crewai framework",
            goal="",
            backstory="",
            allow_delegation=True,
            verbose=True,
            llm=llm4o
        )
        
class Classifier(Agent):
    def __init__(self):
        super().__init__(
            role="Classifier",
            goal="Classify the request into different coding needs, webdev, automation, ",
            backstory="You're an experienced project manager, skilled in defining a prompt short and specific so the team can fulfill the user request",
            allow_delegation=True,
            verbose=True,
            llm=llm4o
        )

class ArchitectAgent(Agent):
    def __init__(self):
        super().__init__(
            role='System Architect',
            goal='Design simple and flexible architectures, you focus on making as few files as possible to be simplistic.',
            backstory="Architect creating basic structures for software projects. You do not comment, just ouput the structure.",
            tools=[],
            verbose=True,
            llm=llm4o
        )

class DeveloperAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Software Developer',
            goal='Implement features with clean, adaptable code. You always make sure that you are writing to the correct file path by tracking the architecture, check the code if there is any before improving it',
            backstory="Developer writing efficient code within defined structures, you are a proffessional who never leaves things unfinished or half done, you love pushing the limits.",
            tools=[FileOperationTool(), HumanInputTool()],
            verbose=True,
            llm=llm4o
        )

class CodeReviewerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Code Reviewer',
            goal='You must ensure that the code is fully finished with no code placeholders. Review code for quality and best practices, ensure the full job is done. **If you can not read a file try checking file path twice and if nothing, continue**.',
            backstory="Reviewer ensuring code meets quality standards, give feedback to the deeloper agent. Famous for being intolerant with basic code and wants the best proffessional efficiency without redundancies or corporative code.",
            tools=[FileOperationTool(), CodeInterpreterTool()],
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

class ClassifierAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Automation Classifier",
            goal="Classify the automation request into specific categories and identify the required specialized agents",
            backstory="Expert in various automation domains, capable of analyzing requests and determining the best approach",
            tools=[HumanInputTool()],
            verbose=True,
            llm=llm4o
        )

class WebAutomationAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Web Automation Specialist",
            goal="Implement web automation scripts using tools like Selenium or Playwright",
            backstory="Expert in web scraping, form filling, and browser automation",
            tools=[FileOperationTool(), HumanInputTool()],
            verbose=True,
            llm=llm4o
        )
        
class APIIntegrationAgent(Agent):
    def __init__(self):
        super().__init__(
            role="API Integration Specialist",
            goal="Create scripts to interact with various APIs and integrate data flows",
            backstory="Expert in API authentication, requests, and data handling",
            tools=[FileOperationTool(), HumanInputTool()],
            verbose=True,
            llm=llm4o
        )
