"""Usage tracking for time and cost monitoring."""

import time
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class APIUsage:
    """Track API call usage."""
    agent_name: str
    phase: str
    timestamp: float
    input_tokens: int = 0
    output_tokens: int = 0
    model: str = ""


@dataclass
class UsageSummary:
    """Summary of usage statistics."""
    start_time: float
    end_time: float = 0
    total_duration: float = 0
    api_calls: List[APIUsage] = field(default_factory=list)
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    estimated_cost: float = 0.0
    
    def calculate_duration(self):
        """Calculate total duration."""
        if self.end_time > 0:
            self.total_duration = self.end_time - self.start_time
    
    def calculate_tokens(self):
        """Calculate total tokens."""
        self.total_input_tokens = sum(call.input_tokens for call in self.api_calls)
        self.total_output_tokens = sum(call.output_tokens for call in self.api_calls)
    
    def calculate_cost(self, model: str = "google/gemini-2.0-flash-001"):
        """Calculate estimated cost based on OpenRouter model pricing.
        
        Pricing (approximation):
        - google/gemini-2.0-flash-001: $0.10/1M input, $0.40/1M output
        - google/gemini-2.0-pro-exp: $0.00/1M (Free tier / Low)
        - openai/gpt-4o-mini: $0.15/1M input, $0.60/1M output
        - meta-llama/llama-3.1-405b: $2.00/1M input, $2.00/1M output
        """
        pricing = {
            "google/gemini-2.0-flash-001": {
                "input": 0.10 / 1_000_000,
                "output": 0.40 / 1_000_000
            },
            "google/gemini-2.0-pro-exp": {
                "input": 0.00 / 1_000_000,
                "output": 0.00 / 1_000_000
            },
            "openai/gpt-4o-mini": {
                "input": 0.15 / 1_000_000,
                "output": 0.60 / 1_000_000
            },
            "meta-llama/llama-3.1-405b": {
                "input": 2.00 / 1_000_000,
                "output": 2.00 / 1_000_000
            }
        }
        
        # Handle model name variations or fallback
        model_key = model.lower()
        if model_key not in pricing:
            # Default to gemini-flash pricing if unknown
            model_key = "google/gemini-2.0-flash-001"
            
        model_pricing = pricing.get(model_key, pricing["google/gemini-2.0-flash-001"])
        input_cost = self.total_input_tokens * model_pricing["input"]
        output_cost = self.total_output_tokens * model_pricing["output"]
        self.estimated_cost = input_cost + output_cost


class UsageTracker:
    """Track usage statistics."""
    
    def __init__(self):
        self.summary = UsageSummary(start_time=time.time())
    
    def record_api_call(self, agent_name: str, phase: str, model: str = "gemini-pro",
                       input_tokens: int = 0, output_tokens: int = 0):
        """Record an API call.
        
        Args:
            agent_name: Name of the agent making the call
            phase: Phase name (e.g., "Demand Analysis")
            model: Model name used
            input_tokens: Number of input tokens (0 if unknown)
            output_tokens: Number of output tokens (0 if unknown)
        """
        usage = APIUsage(
            agent_name=agent_name,
            phase=phase,
            timestamp=time.time(),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model=model
        )
        self.summary.api_calls.append(usage)
    
    def estimate_tokens_from_text(self, text: str) -> int:
        """Estimate token count from text (rough approximation: ~4 chars per token).
        
        Args:
            text: Text to estimate tokens for
            
        Returns:
            Estimated token count
        """
        if not text:
            return 0
        # Rough approximation: 1 token ≈ 4 characters
        return len(text) // 4
    
    def record_api_call_with_text(self, agent_name: str, phase: str, model: str,
                                  input_text: str = "", output_text: str = ""):
        """Record an API call by estimating tokens from text.
        
        Args:
            agent_name: Name of the agent
            phase: Phase name
            model: Model name
            input_text: Input text (for token estimation)
            output_text: Output text (for token estimation)
        """
        input_tokens = self.estimate_tokens_from_text(input_text)
        output_tokens = self.estimate_tokens_from_text(output_text)
        self.record_api_call(agent_name, phase, model, input_tokens, output_tokens)
    
    def finish(self, model: str = "gemini-pro"):
        """Finish tracking and calculate totals.
        
        Args:
            model: Model name for cost calculation
        """
        self.summary.end_time = time.time()
        self.summary.calculate_duration()
        self.summary.calculate_tokens()
        self.summary.calculate_cost(model)
    
    def get_summary(self) -> Dict:
        """Get formatted summary.
        
        Returns:
            Dictionary with usage statistics
        """
        return {
            "duration_seconds": round(self.summary.total_duration, 2),
            "duration_formatted": self._format_duration(self.summary.total_duration),
            "total_api_calls": len(self.summary.api_calls),
            "total_input_tokens": self.summary.total_input_tokens,
            "total_output_tokens": self.summary.total_output_tokens,
            "total_tokens": self.summary.total_input_tokens + self.summary.total_output_tokens,
            "estimated_cost_usd": round(self.summary.estimated_cost, 4),
            "calls_by_phase": self._group_by_phase(),
            "calls_by_agent": self._group_by_agent()
        }
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration as human-readable string.
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
        """
        if seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.2f} minutes"
        else:
            hours = seconds / 3600
            return f"{hours:.2f} hours"
    
    def _group_by_phase(self) -> Dict:
        """Group API calls by phase.
        
        Returns:
            Dictionary with phase statistics
        """
        phases = {}
        for call in self.summary.api_calls:
            if call.phase not in phases:
                phases[call.phase] = {
                    "calls": 0,
                    "input_tokens": 0,
                    "output_tokens": 0
                }
            phases[call.phase]["calls"] += 1
            phases[call.phase]["input_tokens"] += call.input_tokens
            phases[call.phase]["output_tokens"] += call.output_tokens
        return phases
    
    def _group_by_agent(self) -> Dict:
        """Group API calls by agent.
        
        Returns:
            Dictionary with agent statistics
        """
        agents = {}
        for call in self.summary.api_calls:
            if call.agent_name not in agents:
                agents[call.agent_name] = {
                    "calls": 0,
                    "input_tokens": 0,
                    "output_tokens": 0
                }
            agents[call.agent_name]["calls"] += 1
            agents[call.agent_name]["input_tokens"] += call.input_tokens
            agents[call.agent_name]["output_tokens"] += call.output_tokens
        return agents
    
    def print_summary(self):
        """Print formatted summary."""
        summary = self.get_summary()
        print("\n" + "=" * 60)
        print("USAGE SUMMARY")
        print("=" * 60)
        print(f"Total Duration: {summary['duration_formatted']} ({summary['duration_seconds']}s)")
        print(f"Total API Calls: {summary['total_api_calls']}")
        print(f"Total Tokens: {summary['total_tokens']:,}")
        print(f"   - Input:  {summary['total_input_tokens']:,}")
        print(f"   - Output: {summary['total_output_tokens']:,}")
        print(f"Estimated Cost: ${summary['estimated_cost_usd']:.4f} USD")
        print("\nBreakdown by Phase:")
        for phase, stats in summary['calls_by_phase'].items():
            print(f"   {phase}:")
            print(f"      Calls: {stats['calls']}")
            print(f"      Tokens: {stats['input_tokens'] + stats['output_tokens']:,}")
        print("\nBreakdown by Agent:")
        for agent, stats in summary['calls_by_agent'].items():
            print(f"   {agent}:")
            print(f"      Calls: {stats['calls']}")
            print(f"      Tokens: {stats['input_tokens'] + stats['output_tokens']:,}")
        print("=" * 60)

