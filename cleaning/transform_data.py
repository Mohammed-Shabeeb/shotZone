import pandas as pd
import ast

# Step 1: Load the CSV file
file_path = 'output_commentary_labels_1.csv'  # Replace with the actual file path
df = pd.read_csv(file_path)


# Step 2: Define a function to extract attributes from both primary and secondary labels
def extract_attributes(row):
    # Parse the 'output_labels_primary' and 'output_labels_secondary' columns
    primary_labels = ast.literal_eval(row['output_labels_primary'])
    secondary_labels = ast.literal_eval(row['output_labels_secondary'])

    # Initialize attributes with None
    bowler, batsman, length, line, shot_type, position, hit_type, variation, speed, field_activity = [None] * 10

    # Function to parse attributes from the labels
    def parse_labels(labels):
        nonlocal bowler, batsman, length, line, shot_type, position, hit_type, variation, speed, field_activity
        for label in labels:
            if 'Bowler' in label and not bowler:
                bowler = label.split(":")[1].strip()
            elif 'Batsman' in label and not batsman:
                batsman = label.split(":")[1].strip()
            elif 'Speed' in label and not speed:
                speed = label.split(":")[1].strip()
            elif 'Shot Type' in label and not shot_type:
                shot_type = label.split(":")[1].strip()
            elif 'Length' in label and not length:
                length = label.split(":")[1].strip()
            elif 'Line' in label and not line:
                line = label.split(":")[1].strip()
            elif 'Position' in label and not position:
                position = label.split(":")[1].strip()
            elif 'Hit Type' in label and not hit_type:
                hit_type = label.split(":")[1].strip()
            elif 'Variation' in label and not variation:
                variation = label.split(":")[1].strip()
            elif 'Field Activity' in label and not field_activity:
                field_activity = label.split(":")[1].strip()

    # Step 3: First, parse primary labels
    parse_labels(primary_labels)

    # Step 4: If any attribute is not found, fallback to secondary labels
    parse_labels(secondary_labels)

    # Return the parsed attributes
    return pd.Series([bowler, batsman, length, line, shot_type, position, hit_type, variation, speed, field_activity])


# Step 5: Apply the extraction function to the dataframe
df_extracted = df.apply(extract_attributes, axis=1)

# Step 6: Create the final dataframe with extracted attributes and existing ones
df_final = pd.DataFrame({
    'Over': df['ball'].apply(lambda x: str(x).split('.')[0]),  # Split 'ball' into Over
    'Ball No.': df['ball'].apply(lambda x: str(x).split('.')[1] if '.' in str(x) else None),
    # Split 'ball' into Ball No.
    'Bowler': df_extracted[0],
    'Batsman': df_extracted[1],
    'Outcome': df['score'].apply(lambda x: 0 if 'Ã¢â‚¬Â¢' in str(x) else x),  # Assuming score can be mapped to outcome
    'Runs': df['score'].apply(lambda x:
                               0 if x == '•' else
                               6 if x == '6' else
                               int(x[0]) if len(x) == 2 and x[0].isdigit() else
                               int(x) if x.isdigit() else 0),
    'Length': df_extracted[2],
    'Line': df_extracted[3],
    'Shot Type': df_extracted[4],
    'Position': df_extracted[5],
    'Hit Type': df_extracted[6],
    'Variation': df_extracted[7],
    'Speed': df_extracted[8],
    'Field Activity': df_extracted[9]
})

# Step 7: Save the final dataframe to a new CSV file
output_file_path = 'transformed_commentary_data_1.csv'  # Replace with your desired output path
df_final.to_csv(output_file_path, index=False)

print("CSV file has been successfully transformed and saved.")
