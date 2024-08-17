from crewai import Agent
from tools import VSCodeTool, GitTool, CodeAnalysisTool, FileOperationTool, WebScrapingTool, ArchitectureTrackingTool
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
        self.architecture_tool = ArchitectureTrackingTool()
        super().__init__(
            role='System Architect',
            goal='Design and maintain a robust and scalable system architecture',
            backstory="""You're a skilled system architect responsible for
             designing the overall structure of the software system. You ensure
             that the architecture is efficient, maintainable, and aligned with
             project requirements. You also keep track of all project folders and files.""",
            tools=[self.architecture_tool, FileOperationTool()],
            verbose=True,
            llm=llm4o
        )

    def update_architecture(self, item_type: str, path: str, file_type: str = ""):
        if item_type == "folder":
            self.architecture_tool._run("add_folder", path)
        elif item_type == "file":
            self.architecture_tool._run("add_file", path, file_type)

    def get_architecture(self):
        return self.architecture_tool._run("get_structure")

# In agents.py
class DeveloperAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Software Developer',
            goal='Implement high-quality code for the project',
            backstory="""You're a skilled software developer responsible for
             writing efficient and maintainable code. You're currently working
             on implementing new features and fixing bugs, following the project's
             architectural guidelines.""",
            tools=[VSCodeTool(), GitTool(), FileOperationTool(), ArchitectureTrackingTool()],
            verbose=True,
            allow_delegation=True,
            llm=llm4o
        )

    def implement_feature(self, feature_name: str, feature_description: str, architecture: dict):
        # Determine the appropriate location for the new feature
        if "components" in architecture["src"]:
            base_path = f"src/components/{feature_name.lower().replace(' ', '_')}"
        else:
            base_path = f"src/{feature_name.lower().replace(' ', '_')}"

        # Create the main implementation file
        main_file = f"{base_path}/{feature_name.lower().replace(' ', '_')}.py"
        self._create_file(main_file, f"# Implementation of {feature_name}\n\n{feature_description}\n\n# TODO: Implement feature")

        # Create a test file
        test_file = f"src/tests/test_{feature_name.lower().replace(' ', '_')}.py"
        self._create_file(test_file, f"# Tests for {feature_name}\n\n# TODO: Implement tests")

        # Update the architecture
        architecture_tool = ArchitectureTrackingTool()
        architecture_tool._run("add_file", main_file, "Python")
        architecture_tool._run("add_file", test_file, "Python")

        return f"Feature '{feature_name}' implemented in {main_file} with tests in {test_file}"

    def _create_file(self, file_path: str, content: str):
        file_tool = FileOperationTool()
        file_tool._run("write", file_path, content)

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
            goal='Extract relevant information from the web to assist in development tasks',
            backstory="""You are an expert at extracting specific, relevant information from websites. 
            You focus on gathering only the necessary data for the current task, avoiding irrelevant content 
            or examples unless explicitly requested.""",
            tools=[WebScrapingTool(), FileOperationTool()],
            verbose=True,
            llm=llm4o
        )

    def scrape_relevant_info(self, url: str, info_type: str) -> str:
        scraping_tool = WebScrapingTool()
        result = scraping_tool._run(url, info_type)
        
        # Process and filter the result to ensure relevance
        processed_result = self._process_scraped_data(result, info_type)
        
        return processed_result

    def _process_scraped_data(self, data: str, info_type: str) -> str:
        # Implement logic to filter and process the scraped data based on info_type
        # This is a placeholder for more sophisticated processing
        lines = data.split('\n')
        relevant_lines = [line for line in lines if self._is_relevant(line, info_type)]
        return '\n'.join(relevant_lines[:10])  # Limit to top 10 most relevant lines

    def _is_relevant(self, line: str, info_type: str) -> bool:
        # Implement relevance checking logic
        # This is a simple example; you'd want more sophisticated relevance checking in practice
        keywords = {
            "main_content": ["key", "important", "relevant"],
            "headings": ["overview", "summary", "introduction"],
            "links": ["documentation", "api", "reference"],
            "code_snippets": ["function", "class", "method"]
        }
        return any(keyword in line.lower() for keyword in keywords.get(info_type, []))
