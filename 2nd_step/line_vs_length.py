import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
data = pd.read_csv('kohli_overs_6_to_15.csv')

# Filter out rows with missing values for 'Line', 'Length', 'Position', and 'Runs'
data_filtered = data.dropna(subset=['Line', 'Length', 'Position', 'Runs'])

# Create a combined column for Line and Length for the y-axis
data_filtered['Line_Length'] = data_filtered['Line'] + " - " + data_filtered['Length']

# Calculate frequency of each (Line, Length) combination and sum of Runs
combination_stats = data_filtered.groupby(['Line', 'Length']).agg({'Runs': 'sum', 'Position': 'count'}).reset_index()
combination_stats.columns = ['Line', 'Length', 'Total_Runs', 'Count']

# Calculate average runs for each combination
combination_stats['Average_Runs'] = combination_stats['Total_Runs'] / combination_stats['Count']

# Pivot for heatmap with x and y axes swapped
pivot_average_runs = combination_stats.pivot(index="Length", columns="Line", values="Average_Runs")

# Plot heatmap
plt.figure(figsize=(14, 8))
sns.heatmap(pivot_average_runs, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=.5)

# Titles and labels
plt.title('Average Runs Scored by Kohli Against a Particular Length and Line')
plt.xlabel('Delivery Line')
plt.ylabel('Delivery Length')

plt.tight_layout()
plt.show()
