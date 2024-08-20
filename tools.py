import os
from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
import subprocess

class TerminalTool(BaseTool):
    name: str = "Terminal Tool"
    description: str = "Executes terminal commands and performs file operations"

    def _run(self, operation: str, **kwargs) -> str:
        if operation == "execute":
            return self.execute_command(kwargs.get("command", ""))
        elif operation == "find_file":
            return self.find_file(kwargs.get("filename", ""), kwargs.get("directory", "."))
        else:
            return f"Unknown operation: {operation}"

    def execute_command(self, command: str) -> str:
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.stderr}"
        
class ArchitectureTrackingTool(BaseTool):
    name: str = "Architecture Tracking Tool"
    description: str = "Manages project structure and file paths. Operations include set_structure, get_structure."

    def _run(self, operation: str, content: dict = None) -> str:
        """
        Implements the tool's main functionality.
        """
        if operation == "set_structure":
            return self.set_structure(content)
        elif operation == "get_structure":
            return self.get_structure(content.get("project_root", ""))
        else:
            return "Invalid operation. Supported operations: set_structure, get_structure, get_file_path, list_all_files."

    def set_structure(self, content: dict) -> str:
        project_name = content.get("project", "default_project")
        structure = content.get("structure", {})
        
        # Start creating the structure
        
        self.create_project_structure(structure, root_path=project_name)
        return f"Structure created at {project_name}"

    def get_structure(self, project_root: str) -> str:
        try:
            result = subprocess.run(f"tree {project_root}", shell=True, check=True, text=True, capture_output=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error retrieving structure: {e.stderr}"

    def create_project_structure(self, structure: dict, root_path: str):
        """
        Recursively create directories and files based on the provided structure.
        """
        for key, value in structure.items():
            if isinstance(value, list):
                # If value is a list, create files in the current directory
                for item in value:
                    file_path = os.path.join(root_path, item)
                    with open(file_path, 'w') as file:
                        file.write("")  # Create an empty file
            elif isinstance(value, dict):
                # Create directory and recursively create its structure
                directory_path = os.path.join(root_path, key)
                os.makedirs(directory_path, exist_ok=True)
                self.create_project_structure(value, root_path=directory_path)
            elif isinstance(value, str):
                # Create a single file if the value is a string
                file_path = os.path.join(root_path, value)
                with open(file_path, 'w') as file:
                    file.write("")
            else:
                raise ValueError(f"Unexpected structure format: {key} -> {value}")

        
class FileOperationTool(BaseTool):
    name: str = "File Operation Tool"
    description: str = "Handles file reading and writing. The call of function is: (operation: str, file_path: str, content: str)"

    def _run(self, operation: str, file_path: str, content: str) -> str:
        # Ensuring that file operations happen within the 'structures' directory
        file_path = os.path.join("structures", file_path)
        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)

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
                return f"Written to {file_path}"
            except IOError as e:
                return f"Error writing to file: {str(e)}"
        else:
            return "Invalid operation, use read or write."

class WebScrapingTool(BaseTool):
    name: str = "Web Scraping Tool"
    description: str = "Extracts data from web pages"

    def _run(self, url: str, target_info: str) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            if target_info == "main_content":
                main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
                return main_content.get_text(strip=True) if main_content else "Content not found."
            elif target_info == "links":
                return "\n".join(link['href'] for link in soup.find_all('a', href=True))
            return f"Unsupported target_info: {target_info}"
        except requests.RequestException as e:
            return f"Error scraping the web: {str(e)}"
