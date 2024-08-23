import os
from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
import subprocess
from typing import List, Dict, Any
from playwright.sync_api import sync_playwright
import json
import base64

class HumanInputTool(BaseTool):
    name: str = "Human Input Tool"
    description: str = "Requests input from a human user when needed"

    def _run(self, prompt: str) -> str:
        print(f"\nHuman input required: {prompt}")
        return input("Your response: ")
    
def set_architecture(content):

    def create_file(file_path):
        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)
        with open(file_path, 'w') as file:
            file.write("")

    def create_directory(directory_path):
        os.makedirs(directory_path, exist_ok=True)

    def create_project_structure(structure, root_path):
        for key, value in structure.items():
            directory_path = os.path.join(root_path, key)
            create_directory(directory_path)
            if isinstance(value, list):
                for item in value:
                    file_path = os.path.join(directory_path, item)
                    create_file(file_path)
            elif isinstance(value, dict):
                create_project_structure(value, root_path=directory_path)
            else:
                raise ValueError(f"Unexpected structure format: {key} -> {value}")
    
    project_name = content.get("project", "default_project")
    structure = content.get("structure", {})
    create_project_structure(structure, root_path=project_name)

    return project_name

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
        
class FileOperationTool(BaseTool):
    name: str = "File Operation Tool"
    description: str = "Handles file reading and writing. When reading a file, it might be empty and ready to be written."

    def _run(self, operation: str, file_path: str, content: str, project_name: str) -> str:
        
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
        
class HTMLExtractionTool(BaseTool):
    name: str = "HTML Extraction Tool"
    description: str = "Extracts the HTML content from the most relevant link of web searches related to provided queries for automation tasks."

    def _run(self, queries: List[str], max_results: int = 3) -> Dict[str, str]:
        html_data = {}
        for query in queries:
            try:
                important_link = self.search_and_get_first_important_link(query, max_results)
                html_content = self.fetch_page_content(important_link)
                html_data[query] = html_content
            except Exception as e:
                html_data[query] = {"error": f"Error during HTML extraction for query '{query}': {str(e)}"}
        return html_data

    def search_and_get_first_important_link(self, query: str, max_results: int = 3) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            search_url = f"https://www.google.com/search?q={query}"
            page.goto(search_url)

            # Wait for search results to load
            page.wait_for_selector('a', timeout=10000)

            # Extract the first non-ad, non-Google result links
            links = page.query_selector_all('a')
            important_links = []
            for link in links:
                href = link.get_attribute('href')
                if href and 'url?q=' in href and not href.startswith('/'):
                    important_link = href.split('url?q=')[1].split('&')[0]
                    if 'webcache.googleusercontent.com' not in important_link and 'google.com/search' not in important_link:
                        important_links.append(important_link)
                        if len(important_links) >= max_results:
                            break

            browser.close()

            if not important_links:
                raise Exception("No valid links found")

            return important_links[0]

    def fetch_page_content(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching page content from '{url}': {str(e)}")

class DocumentationExtractionTool(BaseTool):
    name: str = "Documentation Extraction Tool"
    description: str = "Extracts relevant documentation from the most relevant link of web searches related to provided queries, such as API endpoints and usage examples."

    def _run(self, queries: List[str], max_results: int = 3, max_code_snippets: int = 3) -> Dict[str, Dict[str, List[str]]]:
        documentation_data = {}
        for query in queries:
            try:
                important_link = self.search_and_get_first_important_link(query, max_results)
                html_content = self.fetch_page_content(important_link)
                documentation_details = self.extract_relevant_documentation(html_content, max_code_snippets)
                documentation_data[query] = documentation_details
            except Exception as e:
                documentation_data[query] = {"error": f"Error during documentation extraction for query '{query}': {str(e)}"}
        return documentation_data

    def search_and_get_first_important_link(self, query: str, max_results: int = 3) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            search_url = f"https://www.google.com/search?q={query}"
            page.goto(search_url)

            # Wait for search results to load
            page.wait_for_selector('a', timeout=10000)

            # Extract the first non-ad, non-Google result links
            links = page.query_selector_all('a')
            important_links = []
            for link in links:
                href = link.get_attribute('href')
                if href and 'url?q=' in href and not href.startswith('/'):
                    important_link = href.split('url?q=')[1].split('&')[0]
                    if 'webcache.googleusercontent.com' not in important_link and 'google.com/search' not in important_link:
                        important_links.append(important_link)
                        if len(important_links) >= max_results:
                            break

            browser.close()

            if not important_links:
                raise Exception("No valid links found")

            return important_links[0]

    def fetch_page_content(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching page content from '{url}': {str(e)}")

    def extract_relevant_documentation(self, html_content: str, max_code_snippets: int = 3) -> Dict[str, List[str]]:
        soup = BeautifulSoup(html_content, 'html.parser')
        code_snippets = [pre.get_text() for pre in soup.find_all('pre')][:max_code_snippets]
        headers = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
        return {'headers': headers, 'code_snippets': code_snippets}
    