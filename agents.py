from crewai import Agent
from tools import VSCodeTool, GitTool, CodeAnalysisTool, FileOperationTool, WebScrapingTool
import os
from langchain_openai import ChatOpenAI
import json


llm4o = ChatOpenAI(model="chatgpt-4o-latest")
llm4o_mini = ChatOpenAI(model="gpt-3.5-turbo")

class ProjectManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Project Manager',
            goal='Manage the software development project efficiently',
            backstory="""You're an experienced project manager overseeing 
            the development of a software project. Your job is to coordinate 
            tasks, ensure deadlines are met, and facilitate communication 
            between team members.""",
            tools=[FileOperationTool()],
            verbose=True,
            llm=llm4o
        )

class ArchitectAgent(Agent):
    def __init__(self):
        super().__init__(
            role='System Architect',
            goal='Design a robust and scalable system architecture',
            backstory="""You're a skilled system architect responsible for 
            designing the overall structure of the software system. You ensure 
            that the architecture is efficient, maintainable, and aligned with 
            project requirements.""",
            tools=[FileOperationTool()],
            verbose=True,
            llm=llm4o
        )

class DeveloperAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Software Developer',
            goal='Implement high-quality code',
            backstory="""You're a skilled software developer responsible for 
            writing efficient and maintainable code. You're currently working 
            on implementing new features and fixing bugs.""",
            tools=[VSCodeTool(), GitTool(), FileOperationTool()],
            verbose=True,
            allow_delegation=True,
            llm=llm4o
        )

class CodeReviewerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Code Reviewer',
            goal='Ensure code quality and adherence to standards',
            backstory="""You're an experienced code reviewer tasked with 
            maintaining high code quality standards. You review code for 
            efficiency, readability, and adherence to best practices.""",
            tools=[CodeAnalysisTool(), FileOperationTool()],
            verbose=True,
            llm=llm4o
        )

class DevOpsAgent(Agent):
    def __init__(self):
        super().__init__(
            role='DevOps Engineer',
            goal='Streamline development operations and ensure smooth deployments',
            backstory="""You're a DevOps engineer responsible for managing 
            the development infrastructure, automating processes, and ensuring 
            smooth deployments. You work closely with developers to optimize 
            the development pipeline.""",
            tools=[GitTool(), FileOperationTool()],
            verbose=True,
            llm=llm4o
        )

class WebScrapingAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Web Scraper',
            goal='Extract necessary information from the web to assist in development tasks',
            backstory="""You specialize in extracting data from websites, 
            including gathering documentation, finding code examples, and scraping 
            elements for automated testing.""",
            tools=[WebScrapingTool(), FileOperationTool()],
            verbose=True,
            llm=llm4o
        )
