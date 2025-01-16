

import pandas as pd

# Load the two CSV files
df1 = pd.read_csv('../16_1_2025/in/info.csv')
df2 = pd.read_csv('../16_1_2025/in/buz.csv')

# Rename the column in df2 before merging
df2 = df2.rename(columns={'commentary': 'second_commentary'})

# Merge the DataFrames
merged_df = pd.merge(df1, df2[['ball', 'second_commentary']], on='ball', how='left')

# Save the result to a new CSV file
merged_df.to_csv('../16_1_2025/in/merged.csv', index=False)

