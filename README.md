# Google ADK Multi-Agent System

A minimal viable multi-agent software development system using Google ADK that replicates ChatDev's core functionality. The system orchestrates multiple specialized agents to develop software from natural language descriptions.

## Features

- **Demand Analysis**: CEO and CPO agents analyze requirements and determine product modality
- **Coding**: CTO and Programmer agents write code based on requirements
- **Code Review**: Automated review loop with Reviewer and Programmer agents
- **Testing**: Automated testing loop with Test Engineer and Programmer agents

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Usage

Run the system with a task description:

```bash
python src/main.py --task "Create a hello world program in Python" --name "hello_world"
```

**Note**: Make sure you're in the project root directory when running this command.

### Command-line Arguments

- `--task`: Task description (required)
- `--name`: Project name (required)
- `--model`: Gemini model to use (default: gemini-pro)
- `--output-dir`: Output directory path (default: ./output)

## Example

```bash
python src/main.py --task "Create a simple calculator with add, subtract, multiply, and divide functions" --name "calculator"
```

The generated code will be saved in the `output/` directory.

## Architecture

The system uses a sequential chain of phases:

1. **Demand Analysis**: Determines product type and requirements
2. **Coding**: Generates initial code
3. **Code Review**: Iterative review and improvement loop
4. **Testing**: Iterative testing and bug fixing loop

Each phase uses specialized agents that communicate through a shared development state.

## Configuration

Agent configurations and prompts can be customized in:
- `config/agent_configs.py`: Agent role definitions and system prompts
- `config/prompts.py`: Phase-specific prompts

## Project Structure

```
google-adk-chatdev/
├── README.md
├── requirements.txt
├── config/
│   ├── agent_configs.py
│   └── prompts.py
├── src/
│   ├── main.py
│   ├── state.py
│   ├── agents/
│   ├── phases/
│   ├── tools/
│   └── chain/
├── output/
└── tests/
```

## License

MIT

