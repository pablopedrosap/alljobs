from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import FileOperationTool, TerminalTool, HTMLExtractionTool, DocumentationExtractionTool

llm4o = ChatOpenAI(model="gpt-4o-mini")

class AgentManager():
    def __init__(self):
        self.pm = ProjectManagerAgent()
        self.architect = ArchitectAgent()
        self.developer = DeveloperAgent()
        self.reviewer = CodeReviewerAgent()
        self.devops = DevOpsAgent()

class ProjectManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Project Manager",
            goal="Efficiently manage the crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.",
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
            goal='Implement features with clean, adaptable code. You always make sure that you are writing to the correct file path by tracking the architecture',
            backstory="Developer writing efficient code within defined structures, you are a proffessional who never leaves things unfinished or half done, you love pushing the limits.",
            tools=[FileOperationTool(), DocumentationExtractionTool(), HTMLExtractionTool()],
            verbose=True,
            llm=llm4o
        )

class CodeReviewerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Code Reviewer',
            goal='You must ensure that the code is fully finished with no code placeholders. Review code for quality and best practices, ensure the full job is done. **If you can not read a file try checking file path twice and if nothing, continue**.',
            backstory="Reviewer ensuring code meets quality standards, give feedback to the deeloper agent. Famous for being intolerant with basic code and wants the best proffessional efficiency without redundancies or corporative code.",
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
