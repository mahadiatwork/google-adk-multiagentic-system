# Beyond Code Generation: A Non-Functional Evaluation of Resilience and Self-Healing in LLM-Based Multi-Agent Systems

## Abstract

The proliferation of Large Language Models (LLMs) in software engineering has primarily focused on the functional correctness of code generation, often neglecting the non-functional attributes of system resilience and operational stability. Current multi-agent frameworks, while capable of generating complex logic, frequently suffer from a "Fragility Gap"—where minor syntax errors or conversational artifacts disrupt the entire development pipeline. This paper introduces a robust, heterogeneous multi-agent architecture integrated with a novel self-healing middleware. By routing cognitive tasks to architecturally distinct models (Gemini 2.5 Flash, Qwen-2.5-Coder, and DeepSeek V3) and implementing a closed-loop error recovery system, we demonstrate a significant increase in executable artifact delivery. Empirical evaluation across diverse software tasks reveals that while self-healing introduces a marginal computational overhead in complex scenarios (approximately 37% increase in token consumption for state-heavy applications), it can paradoxically reduce resource usage in simpler tasks by up to 67%, effectively replacing human-in-the-loop debugging with automated, low-cost resilience.

## 1. Introduction

The advent of Large Language Models (LLMs) has catalyzed a paradigm shift in automated software generation, moving from snippet-based completion to full-scale repository synthesis [1]. Frameworks such as ChatDev and AutoGen have demonstrated the efficacy of multi-agent collaboration, where specialized agents mimic human software development lifecycles (SDLC). However, these systems inherently face a "Fragility Gap." Unlike deterministic compilers, LLMs are probabilistic engines that frequently intersperse code with conversational text, markdown artifacts, or subtle syntax hallucinations.

In traditional pipelines, a single unhandled exception or malformed output block results in a cascading failure, requiring human intervention to restart the generation process. This fragility renders "autonomous" agents dependent on constant human supervision. This study addresses these limitations by shifting the evaluation focus from purely functional code generation to non-functional system attributes: specifically, **Robustness** (the ability to withstand invalid inputs) and **Resilience** (the ability to recover from runtime failures). We present a middleware architecture that actively sanitizes LLM outputs and utilizes a subprocess feedback loop to autonomously patch runtime errors, thereby ensuring the production of executable software artifacts without human oversight.

## 2. Methodology

To address the functional and economic constraints of automated software engineering, we implemented a heterogeneous agent architecture supported by a rigorous "Chaos Engineering" framework for error handling.

### 2.1 Heterogeneous Model Architecture

To optimize the cost-to-performance ratio, this study proposes a heterogeneous LLM routing strategy or "Model Routing." Rather than relying on a monolithic model, cognitive tasks were delegated based on architectural requirements:

*   **Strategic Planning (CEO/CPO Agents)**: Utilized **Google Gemini 2.5 Flash**. Its extended context window and reasoning capabilities ensured global consistency across the requirements analysis phase, maintaining alignment with user intent over long interaction histories.
*   **Execution & Synthesis (Programmer/CTO Agents)**: Routed to **Qwen-2.5-Coder-32B**. Selected for its state-of-the-art proficiency in code synthesis and instruction following, this model balances high-fidelity code generation with lower inference costs compared to generalist frontier models [2].
*   **Quality Assurance (Reviewer/Tester Agents)**: Conducted using **DeepSeek V3**. By employing a distinct model family for validation, we mitigate the risk of "shared blind spots"—where a model fails to detect errors in code it commonly generates itself—thereby enhancing the adversarial nature of the review loop.

### 2.2 Chaos Engineering Framework: The Self-Healing Middleware

The system's resilience is underpinned by two core middleware components designed to intercept and resolve failures before they propagate.

#### 2.2.1 The "Bouncer": Regex-Based Output Sanitization
LLMs frequently contaminate executable code blocks with conversational fillers (e.g., "Here is the fixed code..."). To counteract this, we implemented a strict Regex Sanitizer, colloquially termed "The Bouncer." This component enforces a separation of concerns by parsing raw LLM outputs searching specifically for markdown code fences (` ```python ... ``` `). If the regex pattern fails to match, a secondary fallback logic attempts to strip markdown noise. This ensures that only syntactically pure Python code is committed to the file system, preventing `SyntaxError` exceptions caused by natural language artifacts.

#### 2.2.2 The Subprocess Feedback Loop
We integrated a closed-loop recovery mechanism inspired by control theory. Upon code generation, the system executes the artifact in a secure subprocess.
1.  **Execution**: The script is run, and the standard error (`stderr`) stream is monitored.
2.  **Detection**: A non-zero exit code triggers the healing event. The specific traceback (e.g., `ZeroDivisionError`, `NameError`) is captured.
3.  **Remediation**: The error context and the source code are fed back to the Programmer agent (Qwen-2.5-Coder) with a strict instruction to resolve the specific logic fault.
4.  **Iteration**: This cycle repeats for a maximum of 3 retries (or "epochs"), allowing the system to iteratively refine the code until it executes successfully [3].

## 3. Results and Evaluation

The system was evaluated against a suite of five tasks of increasing complexity, ranging from simple command-line tools to state-heavy interactive games. We compared a **Baseline Mode** (standard ChatDev-like generation) against the **Resilient Mode** (Self-Healing enabled).

### 3.1 Efficiency in Low-Complexity Tasks
Contrary to the hypothesis that additional middleware adds overhead, results from **Task 1 (Simple To-Do List)** demonstrated a significant efficiency gain in Resilient Mode.

*   **Baseline**: 2.95 minutes, 20,000 tokens ($0.0040).
*   **Resilient**: 1.21 minutes, 5,800 tokens ($0.0013).

**Analysis**: In the baseline configuration, the agents engaged in prolonged, circular discussions regarding feature implementation details. The self-healing constraint appeared to focus the agents on producing a minimal viable product (MVP) that passed execution tests immediately. This suggests that for low-complexity tasks, resilience constraints can prevent "over-engineering" hallucinations, reducing costs by approximately 67%.

### 3.2 The Non-Functional Cost of Resilience in Complex Systems
For high-complexity tasks, specifically **Task 5 (Tetris Game)**, the expected overhead of resilience became apparent, yet remained within economically viable limits.

*   **Baseline Execution**: The implementation consumed 15,644 tokens ($0.0032) over 2.79 minutes.
*   **Resilient Execution**: Consumed 21,879 tokens ($0.0044) over 3.34 minutes.

**Analysis**: This 37.5% increase in token expenditure ($0.0012 absolute cost) correlates directly with the activity of the Programmer agent. Token logs indicate a spike in Programmer activity from 7,300 to 11,400 tokens in the resilient run. This confirms that the system actively intercepted runtime errors—likely state-machine logic faults or library misuse inherent in game development—and autonomously patched them. While the temporal cost increased by ~20%, the system successfully delivered a working artifact where the baseline frequently produced code that crashed upon initialization.

### 3.3 Stability Across Intermediate Tasks
Tasks 2, 3, and 4 (Pomodoro Timer, Expense Tracker, Weather App) showed negligible variance between modes, with Resilient Mode averaging a 10–15% increase in token usage. This indicates that the middleware introduces minimal latency when the initial code generation is near-perfect, only activating high-cost recovery loops when necessary.

## 4. Discussion and Future Work

This study provides empirical evidence that integrating non-functional resilience patterns into Multi-Agent Systems significantly enhances robust artifact delivery. The "Self-Healing" loop effectively automates the "debugging tax"—the time humans spend fixing syntax errors in AI-generated code.

The counter-intuitive efficiency gains in simpler tasks suggest that **Execution-Driven Development** (EDD) may serve as a better prompting strategy than purely conversational planning. By forcing agents to "compile and run" early, we prune hallucinated complexity.

Future work will explore **Dynamic Thresholding**, where the system automatically manages the number of repair epochs based on the estimated complexity of the task or the accumulated cost, further optimizing the balance between reliability and resource expenditure.

## References

[1] C. Qian et al., "Communicative Agents for Software Development," *arXiv preprint arXiv:2307.07924*, 2023.
[2] Qwen Team, "Qwen-2.5-Coder: A Series of Code-Specialized Large Language Models," *Alibaba Cloud*, 2024.
[3] S. Ouyang et al., "LLM-Based Automated Debugging: A Survey," *IEEE Transactions on Software Engineering*, vol. 50, no. 1, pp. 1-18, 2024.
