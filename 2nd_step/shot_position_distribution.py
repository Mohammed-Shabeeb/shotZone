import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Kohli data from CSV
kohli_data = pd.read_csv('kohli_overs_6_to_15.csv')

# Filter out rows with missing 'Position' values for accurate plotting
filtered_positions = kohli_data.dropna(subset=['Position'])

# Set the plot style for clarity
sns.set(style="whitegrid")

# Plotting distribution of fielding positions
plt.figure(figsize=(15, 6))
position_counts = sns.countplot(data=filtered_positions, x='Position', order=filtered_positions['Position'].value_counts().index, palette="plasma")
plt.title("Distribution of Fielding Positions for Kohli")
plt.xlabel("Field Position")
plt.ylabel("Frequency")
plt.xticks(rotation=90)  # Set rotation to 90 degrees for vertical labels
plt.tight_layout()

# Show the plot
plt.show()
