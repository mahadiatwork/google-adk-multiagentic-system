# OpenRouter Multi-Agent Development System

A specialized multi-agent software development system that uses OpenRouter AI to orchestrate multiple agents (CEO, CPO, CTO, Programmer, Reviewer, and Tester) to develop software from natural language descriptions.

## 🚀 Recent Improvements

- **Dedicated Role Models**: Refactored the architecture to allow specific LLM models for each agent via `.env` overrides. This allows high-IQ models for coding and low-cost models for strategy.
- **Robustness Fixes**: 
    - Resolved `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'` and `UnicodeEncodeError` in Windows terminals.
    - Upgraded `openai` and `httpx` compatibility.
- **Strict Code Parser**: Implemented a stricter code extraction tool (`code_manager.py`) to prevent capturing sentences as filenames and ensure full file content integrity.
- **Advanced Usage Tracking**: Detailed cost and token tracking across all phases and agents, calibrated for the latest OpenRouter models.

## 🛠 Features

- **Demand Analysis**: CEO and CPO agents analyze requirements (`google/gemini-2.5-flash` recommended).
- **Coding**: CTO and Programmer agents write the core implementation (`qwen/qwen-2.5-coder-32b-instruct` recommended).
- **Code Review**: Automated adversarial review loop (`deepseek/deepseek-chat` recommended).
- **Testing**: Automated testing loop that executes local code and fixes bugs based on error reports.

## 📋 Installation

1. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   OPENROUTER_API_KEY="your_api_key"
   
   # === ROLE-SPECIFIC MODELS (Optimized for Budget & IQ) ===
   MODEL_CEO="google/gemini-2.5-flash"
   MODEL_CPO="google/gemini-2.5-flash"
   MODEL_CTO="qwen/qwen-2.5-coder-32b-instruct"
   MODEL_PROGRAMMER="qwen/qwen-2.5-coder-32b-instruct"
   MODEL_REVIEWER="deepseek/deepseek-chat"
   MODEL_TESTER="deepseek/deepseek-chat"
   
   # FALLBACK MODEL
   OPENROUTER_MODEL="google/gemini-2.5-flash"
   ```

## 🎮 Usage

### 1. Interactive Mode
Run the interactive script to build a project step-by-step:
```powershell
python run_project.py
```

### 2. CLI Mode (Direct)
Specify the task and project name via command-line arguments:
```powershell
python src/main.py --task "Create a simple login page with validation" --name "login-page"
```

### Command-line Arguments
- `--task`: Task description (required)
- `--name`: Project name (required)
- `--model`: Base model ID (optional, overrides OPENROUTER_MODEL)
- `--output-dir`: Output directory path (default: `./output`)
- `--max-review-iterations`: Maximum code review iterations (default: 3)
- `--max-test-iterations`: Maximum test iterations (default: 3)

## 🧪 Testing & Verification

To verify your OpenRouter connection and agent initialization:
```powershell
python test_openrouter.py
```
This script checks your API key, model connectivity, and verifies that the `OpenRouterAgent` can successfully communicate with the AI.

## 📂 Project Structure

- `src/agents/`: Specialized agent classes powered by `OpenRouterAgent`.
- `src/phases/`: Multi-agent collaboration workflows (Demand Analysis -> Coding -> Review -> Testing).
- `src/tools/`: Utilities for robust code extraction, file management, and usage tracking.
- `config/`: System prompts for each agent role and global model settings.

## 📄 License
MIT
# multiagentic-ai-google-sdk
