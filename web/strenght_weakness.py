import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def strength_weakness(path):
    # Load your data
    data = pd.read_csv(path)

    # Filter out rows with missing values for 'Line', 'Length', and 'Position'
    data_filtered = data.dropna(subset=['Line', 'Length', 'Position', 'Runs'])

    # Create a combined column for Line and Length for the y-axis
    data_filtered['Line_Length'] = data_filtered['Line'] + " - " + data_filtered['Length']

    # Calculate frequency of each (Line+Length, Position) combination and total frequency for each (Line+Length)
    combination_counts = data_filtered.groupby(['Line_Length', 'Position']).size().reset_index(name='Count')
    total_counts = data_filtered.groupby('Line_Length').size().reset_index(name='Total')

    # Merge data to calculate percentage
    percentage_data = combination_counts.merge(total_counts, on='Line_Length')
    percentage_data['Percentage'] = (percentage_data['Count'] / percentage_data['Total']) * 100

    # Pivot for heatmap
    pivot_percentage_data = percentage_data.pivot(index="Line_Length", columns="Position", values="Percentage")

    # Plot heatmap
    plt.figure(figsize=(14, 8))
    sns.heatmap(pivot_percentage_data, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=.5)

    # Titles and labels
    plt.title('Percentage of Shots Played by Delivery Line-Length and Shot Position')
    plt.xlabel('Shot Position')
    plt.ylabel('Delivery Line - Length')

    plt.tight_layout()
    plt.show()
