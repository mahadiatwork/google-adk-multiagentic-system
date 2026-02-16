import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set professional style
plt.style.use('seaborn-v0_8-whitegrid')

# 1. Dataset Initialization
data = {
    'Task': ['To-Do List', 'Pomodoro', 'Expense Tracker', 'Weather App', 'Tetris'],
    'Baseline_Duration': [2.95, 2.41, 2.69, 2.03, 2.79],
    'Resilient_Duration': [1.21, 2.67, 3.07, 2.33, 3.34],
    'Baseline_Tokens': [20106, 14018, 16423, 11252, 15644],
    'Resilient_Tokens': [5876, 14550, 16976, 13155, 21879]
}

df = pd.DataFrame(data)

# Constants for plotting
x = np.arange(len(df['Task']))
width = 0.35
colors = {'Baseline': '#4C72B0', 'Resilient': '#DD8452'} # Muted Blue and Coral/Orange

# 2. Chart 1: Execution Duration Comparison
fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, df['Baseline_Duration'], width, label='Baseline', color=colors['Baseline'])
rects2 = ax.bar(x + width/2, df['Resilient_Duration'], width, label='Resilient', color=colors['Resilient'])

# Add text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Execution Duration (Minutes)', fontweight='bold')
ax.set_title('Comparison of Execution Duration: Baseline vs. Resilient Mode', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(df['Task'], rotation=15)
ax.legend(frameon=True, shadow=True)

# Add value labels on top of bars
ax.bar_label(rects1, padding=3, fmt='%.2f', fontsize=9)
ax.bar_label(rects2, padding=3, fmt='%.2f', fontsize=9)

plt.tight_layout()
plt.savefig('fig_duration_comparison.png', dpi=300, bbox_inches='tight')
print("Successfully saved fig_duration_comparison.png")

# 3. Chart 2: Token Consumption Comparison
fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, df['Baseline_Tokens'], width, label='Baseline', color=colors['Baseline'])
rects2 = ax.bar(x + width/2, df['Resilient_Tokens'], width, label='Resilient', color=colors['Resilient'])

# Labels and Titles
ax.set_ylabel('Total Token Consumption', fontweight='bold')
ax.set_title('Comparison of Token Usage: Baseline vs. Resilient Mode', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(df['Task'], rotation=15)
ax.legend(frameon=True, shadow=True)

# Add value labels
ax.bar_label(rects1, padding=3, fontsize=9)
ax.bar_label(rects2, padding=3, fontsize=9)

# Format y-axis to show thousands with 'k' or simple comma
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

plt.tight_layout()
plt.savefig('fig_token_comparison.png', dpi=300, bbox_inches='tight')
print("Successfully saved fig_token_comparison.png")
