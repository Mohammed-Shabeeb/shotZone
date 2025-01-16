import pandas as pd

# Sample commentary_to_labels function as defined previously
class MockDoc:
    def __init__(self, text):
        self.text = text
        self.tokens = text.split()

    def __iter__(self):
        return iter(self.tokens)

def mock_nlp(commentary):
    return MockDoc(commentary)

def commentary_to_labels(commentary):
    doc = mock_nlp(commentary)
    labels = []
    bowler = None
    batsman = None

    # Assume the format is "Bowler to Batsman"
    tokens = commentary.split(",")[0].split(" to ")
    if len(tokens) == 2:
        bowler = tokens[0].strip()
        batsman = tokens[1].strip()

    # Define possible terms
    runs_terms = ["four", "six", "out", "dot", "single", "double", "triple", "no ball"]
    shot_types = ["drive", "cut", "pull", "hook", "sweep", "reverse sweep", "scoop", "upper cut"]
    shot_positions = ["cover", "midwicket", "long-on", "long-off", "point", "gully", "slip", "fine leg", "deep cover"]
    lengths = ["full", "short", "good", "yorker", "half-volley", "bouncer", "overpitched"]
    lines = ["off-stump", "leg-stump", "middle-stump", "wide", "body-line"]
    hit_types = ["inside edge", "outside edge", "top-edge", "bottom-edge", "clean hit", "mishit"]
    variations = ["in-swing", "out-swing", "off-cutter", "leg-cutter", "googly", "flipper", "top-spinner", "doosra"]
    speeds = ["slow", "medium", "fast", "pace", "spin"]
    field_activities = ["catch", "dive", "slide", "stop", "throw", "relay throw", "direct hit", "dropped catch", "misfield", "overthrow"]

    for token in doc:
        token_text = token.lower()

        if token_text == bowler.lower():
            labels.append('Bowler')
        elif token_text == batsman.lower():
            labels.append('Batsman')
        elif token_text in runs_terms:
            if token_text == "out":
                labels.append('Outcome: OUT')
            elif token_text == "four":
                labels.append('Runs: 4')
            elif token_text == "six":
                labels.append('Runs: 6')
            elif token_text == "dot":
                labels.append('Outcome: Dot')
            elif token_text == "single":
                labels.append('Runs: 1')
            elif token_text == "double":
                labels.append('Runs: 2')
            elif token_text == "triple":
                labels.append('Runs: 3')
            elif token_text == "no ball":
                labels.append('Outcome: No Ball')
        elif token_text in shot_types:
            labels.append(f'Shot Type: {token_text.capitalize()}')
        elif token_text in shot_positions:
            labels.append(f'Shot Position: {token_text.capitalize()}')
        elif token_text in lengths:
            labels.append(f'Length: {token_text.capitalize()}')
        elif token_text in lines:
            labels.append(f'Line: {token_text.capitalize()}')
        elif token_text in hit_types:
            labels.append(f'Hit Type: {token_text.capitalize()}')
        elif token_text in variations:
            labels.append(f'Variation: {token_text.capitalize()}')
        elif token_text in speeds:
            labels.append(f'Speed: {token_text.capitalize()}')
        elif token_text in field_activities:
            labels.append(f'Field Activity: {token_text.capitalize()}')
        else:
            labels.append('O')  # Label for other (unimportant) words

    return labels

# Step 1: Read the CSV file
file_path = 'Ball by Ball Commentary & Live Score - SL vs IND, 1st T20I_1.csv'  # Change this to the path of your CSV file
df = pd.read_csv(file_path)

# Step 2: Extract commentary from the appropriate column
commentary_series = df['commentary']  # Adjust 'commentary' to your actual column name

# Step 3: Apply the commentary_to_labels function to each commentary
output_labels = commentary_series.apply(commentary_to_labels)

# Step 4: Add the output labels to the DataFrame
df['output_labels'] = output_labels


output_file_path = 'output_commentary_labels.csv'  # Specify the output file path
df.to_csv(output_file_path, index=False)

# Display a message indicating the process is complete
print(f"Output saved to {output_file_path}")