# Usage Tracking Feature

## Overview

The system now tracks **execution time** and **estimated API costs** for each development run. This helps you monitor resource usage and optimize your workflow.

## What's Tracked

### Time Metrics
- **Total Duration**: Complete execution time from start to finish
- **Formatted Display**: Human-readable format (seconds, minutes, or hours)

### Cost Metrics
- **Total API Calls**: Number of agent interactions
- **Token Usage**: 
  - Input tokens (estimated from prompts)
  - Output tokens (estimated from responses)
- **Estimated Cost**: Calculated based on model pricing

### Breakdowns
- **By Phase**: Usage statistics for each development phase
  - Demand Analysis
  - Coding
  - Code Review
  - Testing
- **By Agent**: Usage statistics for each agent type
  - CEO, CPO, CTO
  - Programmer
  - Reviewer
  - Tester

## How It Works

### Automatic Tracking
Usage tracking is **automatic** - no configuration needed! The system:
1. Starts tracking when you run a task
2. Records each API call with estimated tokens
3. Calculates costs based on model pricing
4. Displays a summary at the end

### Token Estimation
Since Google ADK may not expose exact token counts, the system uses:
- **Approximation**: ~4 characters per token
- This provides a reasonable estimate for cost calculation

### Cost Calculation
Pricing is based on current Google Gemini API rates:
- **gemini-pro**: $0.0005/1K input, $0.0015/1K output
- **gemini-1.5-pro**: $1.25/1M input, $5.00/1M output
- **gemini-1.5-flash**: $0.075/1M input, $0.30/1M output
- **gemini-2.0-flash-exp**: Free tier

*Note: Prices may change - check Google's current pricing*

## Example Output

After running a task, you'll see:

```
============================================================
USAGE SUMMARY
============================================================
⏱️  Total Duration: 2.45 minutes (147.23s)
📞 Total API Calls: 8
🔤 Total Tokens: 15,234
   - Input:  8,456
   - Output: 6,778
💰 Estimated Cost: $0.0123 USD

📊 Breakdown by Phase:
   Demand Analysis:
      Calls: 2
      Tokens: 3,456
   Coding:
      Calls: 2
      Tokens: 5,234
   Code Review:
      Calls: 2
      Tokens: 4,123
   Testing:
      Calls: 2
      Tokens: 2,421

🤖 Breakdown by Agent:
   CEO:
      Calls: 1
      Tokens: 1,234
   CPO:
      Calls: 1
      Tokens: 2,222
   CTO:
      Calls: 1
      Tokens: 2,345
   Programmer:
      Calls: 4
      Tokens: 7,890
   Reviewer:
      Calls: 1
      Tokens: 2,123
   Tester:
      Calls: 1
      Tokens: 2,421
============================================================
```

## Accessing Usage Data

### Programmatically
You can access usage data from the state:

```python
from src.state import DevelopmentState

state = DevelopmentState()
# ... run your chain ...

# Get summary dictionary
summary = state.usage_tracker.get_summary()
print(f"Duration: {summary['duration_formatted']}")
print(f"Cost: ${summary['estimated_cost_usd']}")

# Print formatted summary
state.usage_tracker.print_summary()
```

### Command Line
Usage summary is automatically displayed after each run when using:
```bash
python src/main.py --task "your task" --name "project_name"
```

## Tips for Cost Optimization

1. **Use Faster Models**: `gemini-1.5-flash` is cheaper and faster for simple tasks
2. **Reduce Iterations**: Lower `--max-review-iterations` and `--max-test-iterations` for testing
3. **Monitor Usage**: Check the summary after each run to understand cost patterns
4. **Batch Similar Tasks**: Group related tasks to optimize API usage

## Notes

- Token counts are **estimates** based on text length
- Actual costs may vary slightly from estimates
- Free tier models (like gemini-2.0-flash-exp) show $0.00 cost
- Time tracking is accurate to the second

## Future Enhancements

Potential improvements:
- Export usage data to CSV/JSON
- Historical usage tracking across sessions
- Budget alerts and limits
- More accurate token counting (if ADK provides it)





