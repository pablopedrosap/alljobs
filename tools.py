import subprocess
import os
from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
<<<<<<< HEAD
from urllib.parse import urlparse
import re
from pydantic import BaseModel, Field
from typing import Dict, Any

class ArchitectureTrackingTool(BaseModel):
    name: str = Field(default="Architecture Tracking Tool")
    description: str = Field(default="Tracks and manages project architecture, folders, and files")
    architecture: Dict[str, Any] = Field(default_factory=lambda: {
        "src": {
            "components": {},
            "utils": {},
            "services": {},
            "tests": {}
        },
        "docs": {},
        "config": {}
    })

    def run(self, operation: str, path: str = "", file_type: str = "") -> str:
        if operation == "add_file":
            return self._add_file(path, file_type)
        elif operation == "get_structure":
            return self._get_structure_string()
        else:
            return "Invalid operation. Use 'add_file' or 'get_structure'."

    def _add_file(self, path: str, file_type: str) -> str:
        parts = path.split('/')
        current = self.architecture
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = file_type
        return f"File added: {path} (Type: {file_type})"

    def _get_structure_string(self, structure: Dict[str, Any] = None, indent: int = 0) -> str:
        if structure is None:
            structure = self.architecture
        result = ""
        for key, value in structure.items():
            result += "  " * indent + key + "\n"
            if isinstance(value, dict):
                result += self._get_structure_string(value, indent + 1)
        return result
    
=======

>>>>>>> origin/main

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
<<<<<<< HEAD
    name: str = "Improved Git Operations Tool"
    description: str = "Performs Git operations with better error handling and abstraction"

    def _run(self, operation: str, retry_count: int = 3) -> str:
        for attempt in range(retry_count):
            try:
                result = subprocess.run(f"git {operation}", shell=True, check=True, capture_output=True, text=True)
                return f"Git operation executed successfully: {result.stdout}"
            except subprocess.CalledProcessError as e:
                if attempt == retry_count - 1:
                    return f"Error executing Git operation after {retry_count} attempts: {e.stderr}"
                time.sleep(2)  # Wait before retrying

    def commit_changes(self, message: str) -> str:
        return self._run(f"commit -am '{message}'")

    def push_to_remote(self, branch: str = "main") -> str:
        return self._run(f"push origin {branch}")

=======
    name: str = "Git Operations Tool"
    description: str = "Performs Git operations for version control"

    def _run(self, operation: str) -> str:
        try:
            result = subprocess.run(f"git {operation}", shell=True, check=True, capture_output=True, text=True)
            return f"Git operation executed: {result.stdout}"
        except subprocess.CalledProcessError as e:
            return f"Error executing Git operation: {e.stderr}"
>>>>>>> origin/main

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
<<<<<<< HEAD
                    content = file.read()
                    return content if content else "File is empty"
=======
                    return file.read()
>>>>>>> origin/main
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
<<<<<<< HEAD
    description: str = "Tool to scrape web pages and extract relevant data"

    def _run(self, url: str, target_info: str) -> str:
=======
    description: str = "Tool to scrape web pages and extract data"

    def _run(self, url: str, element: str = None) -> str:
>>>>>>> origin/main
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
<<<<<<< HEAD

            # Extract domain for potential filtering
            domain = urlparse(url).netloc

            # Define extraction strategies based on target_info
            extraction_strategies = {
                "main_content": self._extract_main_content,
                "headings": self._extract_headings,
                "links": self._extract_links,
                "code_snippets": self._extract_code_snippets
            }

            if target_info in extraction_strategies:
                return extraction_strategies[target_info](soup, domain)
            else:
                return f"Unsupported target_info: {target_info}. Please use one of: {', '.join(extraction_strategies.keys())}"

        except requests.RequestException as e:
            return f"Error scraping the web: {str(e)}"

    def _extract_main_content(self, soup, domain):
        # Attempt to find the main content area
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main'))
        if main_content:
            return main_content.get_text(strip=True)
        return "Main content could not be identified."

    def _extract_headings(self, soup, domain):
        headings = soup.find_all(['h1', 'h2', 'h3'])
        return "\n".join([h.get_text(strip=True) for h in headings])

    def _extract_links(self, soup, domain):
        links = soup.find_all('a', href=True)
        relevant_links = [link['href'] for link in links if domain in link['href'] or link['href'].startswith('/')]
        return "\n".join(relevant_links)

    def _extract_code_snippets(self, soup, domain):
        code_snippets = soup.find_all('code')
        return "\n\n".join([snippet.get_text(strip=True) for snippet in code_snippets])

=======
            if element:
                data = soup.select(element)
                return '\n'.join([str(elem) for elem in data])
            return soup.prettify()
        except requests.RequestException as e:
            return f"Error scraping the web: {str(e)}"
>>>>>>> origin/main
        
class CodeGenerationTool(BaseTool):
    name: str = "Code Generation Tool"
    description: str = "Generates code snippets based on provided inputs"

    def _run(self, template: str, context: dict) -> str:
        # Simplified code generation example
        code = template.format(**context)
        return code