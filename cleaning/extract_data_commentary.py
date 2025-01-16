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

    # Assume the format is "Bowler to Batsman"
    tokens = commentary.split(",")[0].split(" to ")
    if len(tokens) == 2:
        bowler = tokens[0].strip()
        batsman = tokens[1].strip()

    # Split the names into words for checking
    bowler_tokens = bowler.lower().split()
    batsman_tokens = batsman.lower().split()

    # Define possible terms
    runs_terms = {"four", "4", "six", "6", "out", "dot", "0", "single", "1", "double", "2", "triple", "3", "5", "no ball"}
    shot_types = {"drive", "cut", "pull", "hook", "sweep", "reverse-sweep", "scoop", "upper-cut", "straight-drive",
                  "cover-drive", "on-drive", "off-drive", "defensive-shot", "square-drive", "cut-shot", "pull-shot",
                  "hook-shot", "backfoot-defence", "square-cut", "scoop-shot", "ramp-shot", "flick-shot", "glance"}
    shot_positions = {"slip", "second-slip", "fly-slip", "gully", "short-third-man", "backward-point", "point",
                      "deep-point", "deep-backward-point", "cover", "extra-cover", "deep-cover", "deep-extra-cover",
                      "mid-off", "long-off", "straight-hit", "mid-on", "long-on", "cow-corner", "deep-mid-wicket",
                      "midwicket", "short-leg", "silly-mid-off", "silly-mid-on", "silly-point", "short-fine-leg",
                      "fine-leg", "deep-fine-leg", "long-leg", "backward-square-leg", "square-leg", "leg-gully",
                      "third-man", "long-stop", "deep-square", "deep-square-leg", "deep-third"}
    lengths = {"full", "good", "short", "yorker", "length"}
    lines = {"outside-off", "leg-stump", "middle-stump"}
    hit_types = {"clean-hit","inside-edge", "outside-edge", "top-edge", "bottom-edge", "mishit", "thick-edge", "thin-edge", "miss-hit"}
    variations = {"in-swing", "out-swing", "off-cutter", "leg-cutter", "googly", "flipper", "top-spinner", "doosra",
                  "wrong'un", "slider", "carrom-ball"}
    speeds = {"slow", "medium", "fast", "pace", "spin", "slower", "faster"}
    field_activities = {"catch", "dive", "slide", "stop", "throw", "relay-throw", "direct-hit", "dropped-catch",
                        "misfield", "overthrow", "run-out", "stumping", "hit-wicket", "bowled", "leg-before-wicket",
                        "fielding-error", "miss-field"}

    # Tokenize the commentary
    token_list = list(doc)

    # Initialize flags to check if we have identified the bowler and batsman
    bowler_identified = False
    batsman_identified = False

    # List to keep track of detected shot positions
    detected_positions = []

    # Iterate over tokens in the token_list
    for token in token_list:
        token_text = token.lower()

        # Match the bowler's name
        if not bowler_identified and token_text in bowler_tokens:
            labels.append(f'Bowler: {bowler}')
            bowler_identified = True

        # Match the batsman's name
        elif not batsman_identified and token_text in batsman_tokens:
            labels.append(f'Batsman: {batsman}')
            batsman_identified = True

        # Check for matches in various term categories
        elif token_text in runs_terms:
            labels.append(f'Runs: {token_text}' if token_text.isdigit() else f'Outcome: {token_text.capitalize()}')
        elif token_text in shot_types:
            labels.append(f'Shot Type: {token_text.capitalize()}')
        elif token_text in shot_positions:
            detected_positions.append(token_text.capitalize())
        elif token_text not in shot_positions and token_text[:-1] in shot_positions:
            detected_positions.append(token_text[:-1].capitalize())
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

    # Add detected shot positions if found
    if detected_positions:
        labels.append(f'Shot Position: {detected_positions[0]}')

    # Check for special positions if no standard positions found
    if not detected_positions:
        for special_position in ["leg-side", "off-side", "on-side"]:
            if special_position in token_list:
                labels.append(f'Shot Position: {special_position.capitalize()}')
                break

    labels.append(f'Batsman: {batsman}')
    return labels


# Step 1: Read the CSV file
file_path = 'Ind_vs_Aus_26_nov_2023_ind_batting_updated.csv'  # Change this to the path of your CSV file
df = pd.read_csv(file_path)

# Step 2: Extract commentary from the appropriate columns
primary_commentary_series = df['commentary']
secondary_commentary_series = df['second_commentary']

# Step 3: Apply the commentary_to_labels function to each commentary in both columns
output_labels_primary = primary_commentary_series.apply(commentary_to_labels)
output_labels_secondary = secondary_commentary_series.apply(commentary_to_labels)

# Step 4: Add the output labels to the DataFrame
df['output_labels_primary'] = output_labels_primary
df['output_labels_secondary'] = output_labels_secondary

# Save the output to a new CSV file
output_file_path = 'output_commentary_labels_1.csv'
df.to_csv(output_file_path, index=False)

print(f"Output saved to {output_file_path}")
