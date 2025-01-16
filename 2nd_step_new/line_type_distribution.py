import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Kohli data from CSV
kohli_data = pd.read_csv('kohli_overs_6_to_15.csv')

# Filter out rows with missing 'Line' values for accurate plotting
filtered_lines = kohli_data.dropna(subset=['Line'])

# Set the plot style for clarity
sns.set(style="whitegrid")

# Calculate the counts of each line type
line_type_counts = filtered_lines['Line'].value_counts()

# Create a pie chart
plt.figure(figsize=(10, 6))
plt.pie(line_type_counts, labels=line_type_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("crest", n_colors=len(line_type_counts)))
plt.title("Distribution of Line Types for Kohli")
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Show the plot
plt.tight_layout()
plt.show()
