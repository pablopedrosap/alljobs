import os
from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup

class ArchitectureTrackingTool(BaseTool):
    name: str = "Architecture Tracking Tool"
    description: str = "Manages project structure and file paths, operation is set_structure or get_structure"
    structure: dict = {}

    def _run(self, operation: str, content: dict = None) -> str:
        if operation == "set_structure":
            self.structure = content
            self.create_project_structure(self.structure)
            return "Structure created."
        elif operation == "get_structure":
            return str(self.structure)
        return "Invalid operation, use set_structure or get_structure."

    def create_project_structure(self, structure: dict, root_path: str = "."):
        for key, value in structure.items():
            path = os.path.join(root_path, key)
            if isinstance(value, dict):
                os.makedirs(path, exist_ok=True)
                self.create_project_structure(value, root_path=path)
            else:
                file_path = os.path.join(path, value)
                with open(file_path, 'w') as file:
                    pass

class FileOperationTool(BaseTool):
    name: str = "File Operation Tool"
    description: str = "Handles file reading and writing"

    def _run(self, operation: str, file_path: str, content: str = "") -> str:
        # Ensuring that file operations happen within the 'structure' directory
        file_path = os.path.join("structure", file_path)
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
