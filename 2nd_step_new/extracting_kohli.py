import pandas as pd
import glob

# Define a list of possible names for the batsman
batsman_names = ["virat kohli", "virat", "kohli", "vk", "v k", "v kohli"]  # Replace with actual name variations

# Use glob to find all CSV files in the specified directory
file_paths = glob.glob("./*.csv")

# Initialize an empty list to store dataframes
batsman_data = []

# Process each file
for file_path in file_paths:
    # Load the CSV file
    df = pd.read_csv(file_path)
    df = df.drop_duplicates()
   
    # Filter for rows where the Batsmen column matches any of the names in batsman_names
    filtered_df = df[df['Batsman'].isin(batsman_names)]
   
    # Append the filtered data to our list if any rows match
    if not filtered_df.empty:
        batsman_data.append(filtered_df)

# Concatenate all DataFrames in the batsman_data list into a single DataFrame
final_data = pd.concat(batsman_data, ignore_index=True)

# Save the final data to a CSV file
final_data.to_csv("kohli.csv", index=False)

# Create partitions based on overs
# Ensure there's a column named 'Over' in the DataFrame for filtering
if 'Over' in final_data.columns:
    # Filter for overs < 6
    over_less_6 = final_data[final_data['Over'] < 6]
    over_less_6.to_csv("kohli_overs_less_than_6.csv", index=False)
    
    # Filter for 6 <= overs < 15
    over_6_to_15 = final_data[(final_data['Over'] >= 6) & (final_data['Over'] < 15)]
    over_6_to_15.to_csv("kohli_overs_6_to_15.csv", index=False)
    
    # Filter for overs >= 15
    over_15 = final_data[final_data['Over'] >= 15]
    over_15.to_csv("kohli_overs_greater_than_15.csv", index=False)

print("Filtered data has been saved to 'kohli.csv' and additional files have been created based on overs.")
