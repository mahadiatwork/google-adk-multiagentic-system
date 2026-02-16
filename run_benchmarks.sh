#!/bin/bash

# ==============================================================================
# LLM Multi-Agent System Benchmarking Suite
# ==============================================================================
# Description: Automates evaluation of Baseline vs. Resilient (Self-Healing) modes.
# Usage: ./run_benchmarks.sh
# Note: REMEMBER TO RUN: chmod +x run_benchmarks.sh
# ==============================================================================

# Initialize CSV Log
CSV_FILE="benchmark_results.csv"
OUTPUT_DIR="benchmark_output"
echo "Task_ID,Task_Name,Mode,Exit_Code,Status" > "$CSV_FILE"

# Prepare Benchmark Output Directory
if [ -d "$OUTPUT_DIR" ]; then
    echo "Cleaning existing benchmark output..."
    rm -rf "$OUTPUT_DIR"
fi
mkdir -p "$OUTPUT_DIR"

# Define Test Cases
declare -A PROMPTS
PROMPTS[1]="Simple To-Do list with add/remove functionality"
PROMPTS[2]="Pomodoro Timer with start/reset and notification"
PROMPTS[3]="CLI Expense Tracker with CSV storage"
PROMPTS[4]="Weather App using a mock API and colorful output"
PROMPTS[5]="Playable Tetris game in the terminal"

# Styling
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}====================================================${NC}"
echo -e "${CYAN}   🚀 STARTING MULTI-AGENT SYSTEM BENCHMARKS       ${NC}"
echo -e "${CYAN}====================================================${NC}"

for i in {1..5}
do
    TASK_PROMPT="${PROMPTS[$i]}"
    echo -e "\n${YELLOW}[TASK $i/5]${NC} ${BLUE}$TASK_PROMPT${NC}"
    
    # ---------------------------------------------------------
    # 1. Baseline Run (No Healing)
    # ---------------------------------------------------------
    MODE="Baseline"
    NAME="task_${i}_baseline"
    
    echo -e "   ${CYAN}├─ Mode:${NC} $MODE..."
    python src/main.py --task "$TASK_PROMPT" --name "$NAME" --output-dir "$OUTPUT_DIR"
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then STATUS="Success"; COL=$GREEN; else STATUS="Failed"; COL=$RED; fi
    echo -e "   ${CYAN}└─ Status:${NC} ${COL}$STATUS${NC} (Exit Code: $EXIT_CODE)"
    echo "$i,$NAME,$MODE,$EXIT_CODE,$STATUS" >> "$CSV_FILE"

    # ---------------------------------------------------------
    # 2. Resilient Run (With Healing)
    # ---------------------------------------------------------
    MODE="Resilient"
    NAME="task_${i}_healing"
    
    echo -e "   ${CYAN}├─ Mode:${NC} $MODE..."
    python src/main.py --task "$TASK_PROMPT" --name "$NAME" --healing --output-dir "$OUTPUT_DIR"
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then STATUS="Success"; COL=$GREEN; else STATUS="Failed"; COL=$RED; fi
    echo -e "   ${CYAN}└─ Status:${NC} ${COL}$STATUS${NC} (Exit Code: $EXIT_CODE)"
    echo "$i,$NAME,$MODE,$EXIT_CODE,$STATUS" >> "$CSV_FILE"
done

echo -e "\n${CYAN}====================================================${NC}"
echo -e "${GREEN}   ✅ BENCHMARK COMPLETE! Results saved to:${NC}"
echo -e "${YELLOW}   $CSV_FILE${NC}"
echo -e "${CYAN}====================================================${NC}"