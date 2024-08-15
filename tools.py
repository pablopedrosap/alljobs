import subprocess
import os
from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup


class VSCodeTool(BaseTool):
    name: str = "VS Code Interaction Tool"
    description: str = "Interacts with VS Code to perform coding tasks"

    def _run(self, command: str) -> str:
        try:
            result = subprocess.run(f"code {command}", shell=True, check=True, capture_output=True, text=True)
            return f"VS Code command executed: {result.stdout}"
        except subprocess.CalledProcessError as e:
            return f"Error executing VS Code command: {e.stderr}"

class GitTool(BaseTool):
    name: str = "Git Operations Tool"
    description: str = "Performs Git operations for version control"

    def _run(self, operation: str) -> str:
        try:
            result = subprocess.run(f"git {operation}", shell=True, check=True, capture_output=True, text=True)
            return f"Git operation executed: {result.stdout}"
        except subprocess.CalledProcessError as e:
            return f"Error executing Git operation: {e.stderr}"

class CodeAnalysisTool(BaseTool):
    name: str = "Code Analysis Tool"
    description: str = "Analyzes code for quality and suggests improvements"

    def _run(self, file_path: str) -> str:
        try:
            # Using pylint for Python code analysis
            result = subprocess.run(f"pylint {file_path}", shell=True, capture_output=True, text=True)
            return f"Code analysis result:\n{result.stdout}"
        except subprocess.CalledProcessError as e:
            return f"Error during code analysis: {e.stderr}"

class FileOperationTool(BaseTool):
    name: str = "File Operation Tool"
    description: str = "Performs file operations like reading and writing"

    def _run(self, operation: str, file_path: str, content: str = "") -> str:
        if operation == "read":
            try:
                with open(file_path, 'r') as file:
                    return file.read()
            except IOError as e:
                return f"Error reading file: {str(e)}"
        elif operation == "write":
            try:
                with open(file_path, 'w') as file:
                    file.write(content)
                return f"Content written to {file_path}"
            except IOError as e:
                return f"Error writing to file: {str(e)}"
        else:
            return "Invalid operation. Use 'read' or 'write'."

class WebScrapingTool(BaseTool):
    name: str = "Web Scraping Tool"
    description: str = "Tool to scrape web pages and extract data"

    def _run(self, url: str, element: str = None) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            if element:
                data = soup.select(element)
                return '\n'.join([str(elem) for elem in data])
            return soup.prettify()
        except requests.RequestException as e:
            return f"Error scraping the web: {str(e)}"
        
class CodeGenerationTool(BaseTool):
    name: str = "Code Generation Tool"
    description: str = "Generates code snippets based on provided inputs"

    def _run(self, template: str, context: dict) -> str:
        # Simplified code generation example
        code = template.format(**context)
        return code