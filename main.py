import os
import json
import logging
from typing import Dict, List, Any, Optional
from crewai import Crew, Task, Process
from langchain_openai import ChatOpenAI
from agents import AgentManager
from tools import FileOperationTool, TerminalTool, DocumentationExtractionTool, set_architecture

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AIDevelopmentSystem:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.agent_manager = AgentManager()
        self.file_operation_tool = FileOperationTool()
        self.manager_llm = ChatOpenAI(model=model)
        self.project_structure: Optional[Dict[str, Any]] = None
        logger.info(f"Initialized with model: {model}")

    def classify_task(self, feature_description: str) -> Dict[str, Any]:
        classification_task = Task(
            description=f"Classify the automation task and identify required specialized agents: {feature_description}",
            agent=self.agent_manager.classifier,
            expected_output="JSON with task_type, required_agents, and complexity_level"
        )
        classification_crew = Crew(
            agents=[self.agent_manager.classifier],
            tasks=[classification_task],
            process=Process.sequential
        )
        return classification_crew.kickoff()
    
    def generate_json_plan(self, feature_description: str) -> Dict[str, Any]:
        plan_task = Task(
            description=f"Generate a detailed JSON plan for: {feature_description}. Max 10 super specific steps. No timeline, just actionable steps that can be implemented in code.",
            agent=self.agent_manager.planner,
            output_format="JSON"
        )
        plan_crew = Crew(
            agents=[self.agent_manager.planner],
            tasks=[plan_task],
            process=Process.sequential
        )
        result = plan_crew.kickoff()
        logger.info("Generated execution plan")
        return json.loads(result) if isinstance(result, str) else result

    def _get_default_files(self, project_structure: Dict[str, Any]) -> List[str]:
        """Returns default entry point files when specific files can't be determined."""
        defaults = []
        project_name = project_structure.get('project', '')

        def collect_files(struct: Dict, base_path: str = ""):
            for key, value in struct.items():
                current_path = os.path.join(base_path, key)
                if isinstance(value, list):
                    defaults.extend([os.path.join(current_path, f) for f in value])

        collect_files(project_structure.get('structure', {}), project_name)
        return defaults[:3]

    def create_architect_task(self, json_plan: Dict[str, Any]) -> Task:
        return Task(
            description=f"Design the project structure based on this plan: {json_plan}",
            agent=self.agent_manager.architect,
            output_format="JSON",
            expected_output="""Keep it simple. Output format: {
                "project": "project_name",
                "structure": {
                    "src": ["main.py", "utils.py"],
                    "tests": ["test_main.py"]
                }
            }"""
        )
    def identify_relevant_files(self, step: Dict[str, Any], project_structure: Dict[str, Any]) -> List[str]:
        """Identifies files relevant to the current implementation step."""
        if not project_structure or 'structure' not in project_structure:
            return []

        relevant_files = []
        step_description = step.get('description', '').lower()

        def scan_structure(struct: Dict, base_path: str = ""):
            for key, value in struct.items():
                current_path = os.path.join(base_path, key)
                if isinstance(value, list):
                    for filename in value:
                        file_path = os.path.join(current_path, filename)
                        if any(keyword in file_path.lower() for keyword in step_description.split()):
                            relevant_files.append(file_path)
                elif isinstance(value, dict):
                    scan_structure(value, current_path)

        project_name = project_structure.get('project', '')
        scan_structure(project_structure['structure'], project_name)

        return relevant_files if relevant_files else self._get_default_files(project_structure)

    def execute_step(self, step: Dict[str, Any], relevant_files: List[str],
                     project_structure: Dict[str, Any], json_plan: Dict[str, Any]):
        """Executes a single step across relevant files with review feedback loop."""
        step_desc = step.get('description', str(step))
        logger.info(f"Executing step: {step_desc}")

        classification = self.classify_task(json_plan.get('description', ''))
        agent = self._get_specialized_agent(classification)

        for file_path in relevant_files:
            logger.info(f"Processing file: {file_path}")
            context = f"Project structure: {project_structure}\nCurrent step: {step_desc}"

            max_iterations = 3
            for iteration in range(max_iterations):
                dev_task = Task(
                    description=f"Implement {step_desc} for {file_path}. Use HumanInputTool if you need clarification.",
                    agent=agent,
                    expected_output="Complete implementation code"
                )
                dev_crew = Crew(agents=[agent], tasks=[dev_task], process=Process.sequential)
                implementation = dev_crew.kickoff()

                review_task = Task(
                    description=f"Review implementation of {step_desc} for {file_path}\nContext: {context}",
                    agent=self.agent_manager.reviewer,
                    expected_output="JSON with 'status' (complete/incomplete) and 'feedback' fields"
                )
                review_crew = Crew(agents=[self.agent_manager.reviewer], tasks=[review_task])
                review = review_crew.kickoff()

                if isinstance(review, dict) and review.get('status') == 'complete':
                    logger.info(f"Implementation approved for {file_path}")
                    break
                elif iteration < max_iterations - 1:
                    feedback = review.get('feedback', 'Please address review comments') if isinstance(review, dict) else str(review)
                    context += f"\nReview feedback (iteration {iteration + 1}): {feedback}"
                    logger.warning(f"Review iteration {iteration + 1} for {file_path}")
                else:
                    logger.error(f"Max iterations reached for {file_path}")

    def _get_specialized_agent(self, classification: Dict[str, Any]):
        """Returns the appropriate specialized agent based on task classification."""
        agent_mapping = {
            'web_automation': self.agent_manager.web_automation,
            'api_integration': self.agent_manager.api_integration,
        }

        agent_type = classification.get('task_type', '').lower().replace(' ', '_')
        return agent_mapping.get(agent_type, self.agent_manager.api_integration)

    def run(self, feature_description: str) -> Dict[str, Any]:
        """Main execution pipeline for automated development."""
        try:
            logger.info(f"Starting development pipeline for: {feature_description}")

            json_plan = self.generate_json_plan(feature_description)

            architect_task = self.create_architect_task(json_plan)
            architect_crew = Crew(agents=[self.agent_manager.architect], tasks=[architect_task])
            raw_structure = architect_crew.kickoff()

            project_structure = json.loads(raw_structure) if isinstance(raw_structure, str) else raw_structure
            self.project_structure = project_structure

            project_name = set_architecture(project_structure)
            logger.info(f"Created project structure: {project_name}")

            steps = json_plan.get('steps', [])
            for idx, step in enumerate(steps):
                logger.info(f"Step {idx + 1}/{len(steps)}")
                relevant_files = self.identify_relevant_files(step, project_structure)
                self.execute_step(step, relevant_files, project_structure, json_plan)

            logger.info("Development pipeline completed successfully")
            return {
                'status': 'success',
                'project': project_name,
                'structure': project_structure
            }

        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e)
            }
        

def main():
    ai_system = AIDevelopmentSystem()

    feature_description = """
    Create a rental management automation system that handles:
    - Calendar synchronization across Airbnb and Booking.com
    - Dynamic pricing based on market conditions
    - Automated guest communication workflows
    - Financial reporting and analytics
    """

    result = ai_system.run(feature_description)

    if result['status'] == 'success':
        print(f"\n✓ Project created: {result['project']}")
        print(f"Structure: {json.dumps(result['structure'], indent=2)}")
    else:
        print(f"\n✗ Failed: {result['error']}")

if __name__ == "__main__":
    main()


