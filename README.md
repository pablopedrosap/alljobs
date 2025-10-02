# AI Development System

Multi-agent orchestration system for automated software development. Routes tasks through specialized AI agents to handle planning, architecture, implementation, and code review.

## Architecture

Built on CrewAI with specialized agents for different development domains:

**Core Pipeline**
- `Classifier` → Routes requests to specialized agents
- `Planner` → Generates structured execution plans
- `Architect` → Designs minimal project structures
- `Developer Agents` → Domain-specific implementation (web automation, API integration)
- `Code Reviewer` → Quality control with feedback loops
- `DevOps` → Deployment management

## Features

- Intelligent task classification and agent routing
- Automated project structure generation
- Iterative development with review cycles (max 3 iterations per file)
- Human-in-the-loop for credentials and clarifications
- Structured logging throughout pipeline
- Support for web automation (Playwright) and API integrations

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Configure environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

## Usage

```python
from main import AIDevelopmentSystem

system = AIDevelopmentSystem()

result = system.run("""
Create a web scraper that:
- Extracts product data from e-commerce sites
- Stores results in JSON format
- Handles pagination and rate limiting
""")

if result['status'] == 'success':
    print(f"Project created: {result['project']}")
```

## Project Structure

```
.
├── main.py          # Core orchestration system
├── agents.py        # Agent definitions and configurations
├── tools.py         # Custom tools (file ops, terminal, web extraction)
├── config.py        # Configuration management
└── requirements.txt # Dependencies
```

## How It Works

1. **Classification**: Analyzes the task description and determines required agent types
2. **Planning**: Generates a JSON plan with concrete, actionable steps
3. **Architecture**: Creates a minimal project structure based on the plan
4. **Implementation**: Each step is executed by specialized agents across relevant files
5. **Review Loop**: Code reviewer validates implementations, provides feedback if needed
6. **Iteration**: Failed reviews trigger re-implementation with feedback context (max 3 attempts)

## Technical Stack

- **Framework**: CrewAI for agent orchestration
- **LLM**: OpenAI GPT-4o-mini via LangChain
- **Web Automation**: Playwright (headless browser control)
- **Web Scraping**: BeautifulSoup4, Requests
- **Type Safety**: Python typing annotations throughout

## Agent Details

### Specialized Agents
- **Web Automation Agent**: Selenium/Playwright scripts, form filling, scraping
- **API Integration Agent**: REST/GraphQL clients, authentication, data pipelines

### Support Agents
- **Project Manager**: Refines prompts and coordinates workflow
- **Architect**: Favors simplicity, minimal file structures
- **Code Reviewer**: Enforces completion, no placeholders, professional standards

## Configuration

Environment variables via `.env`:
```bash
OPENAI_API_KEY=sk-...
```

Optional config in `config.py`:
- `DEFAULT_MODEL`: LLM model selection
- `MAX_REVIEW_ITERATIONS`: Review cycle limit
- `LOG_LEVEL`: Logging verbosity

## Design Principles

- **Minimal complexity**: Simple architectures over elaborate ones
- **Iterative quality**: Review feedback loops ensure completeness
- **Context awareness**: Agents track project structure and existing code
- **Fail-safe defaults**: Graceful degradation when file identification fails

## Limitations

- Focused on automation scripts rather than large-scale applications
- Requires OpenAI API access
- Human input may be needed for credentials or ambiguous requirements
- Generated code quality depends on LLM capabilities

## Extension Points

Add new specialized agents by:
1. Define agent class in [agents.py](agents.py) inheriting from `Agent`
2. Register in `AgentManager`
3. Add routing logic in `_get_specialized_agent()` in [main.py](main.py)
4. Equip with domain-specific tools from [tools.py](tools.py)

## Example Use Cases

- Web scraping pipelines with error handling
- API client generation from documentation
- Data processing workflows
- Browser automation for testing
- Multi-platform integrations (Airbnb, Booking.com, etc.)

## Performance

- Pipeline execution time scales with project complexity
- Most automation scripts: 5-15 minutes end-to-end
- Review iterations add 2-3 minutes per failure
- LLM API calls are the primary bottleneck

## License

MIT
