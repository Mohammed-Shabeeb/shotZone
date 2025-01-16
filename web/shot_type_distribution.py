import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def shot_type(path):
    # Load the Kohli data from CSV
    kohli_data = pd.read_csv(path)

    # Filter out data with NaN in the 'Shot Type' column, as they don't provide information for this plot
    filtered_data = kohli_data.dropna(subset=['Shot Type'])

    # Set the plot style for clarity
    sns.set(style="whitegrid")

    # Plotting distribution of shot types using seaborn countplot
    plt.figure(figsize=(10, 6))
    shot_type_counts = sns.countplot(data=filtered_data, x='Shot Type', order=filtered_data['Shot Type'].value_counts().index, palette="viridis")
    plt.title("Distribution of Shot Types for Kohli")
    plt.xlabel("Shot Type")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()
