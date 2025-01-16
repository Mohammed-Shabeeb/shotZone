import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def outcome(path):
    # Load the Kohli data from CSV
    kohli_data = pd.read_csv(path)

    # Replace 'â€¢' with 'Dot' in the Outcome column to standardize values
    kohli_data['Outcome'] = kohli_data['Outcome'].replace('â€¢', 'Dot')


    # Filter out rows with missing values in 'Outcome' for an accurate count
    filtered_outcomes = kohli_data.dropna(subset=['Outcome'])

    # Set the plot style for clarity
    sns.set(style="whitegrid")

    # Plot distribution of outcomes
    plt.figure(figsize=(10, 6))
    outcome_counts = sns.countplot(data=filtered_outcomes, x='Outcome', order=filtered_outcomes['Outcome'].value_counts().index, palette="magma")
    plt.title("Distribution of Outcomes for Kohli")
    plt.xlabel("Outcome")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()
