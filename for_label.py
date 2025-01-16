import spacy

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Predefined lists of common cricket terms
runs_terms = ["four", "six", "out", "dot", "single", "double", "triple", "no ball"]
shot_types = ["drive", "cut", "pull", "hook", "sweep", "reverse sweep", "scoop", "upper cut"]
shot_positions = ["cover", "midwicket", "long-on", "long-off", "point", "gully", "slip", "fine leg", "deep cover"]
lengths = ["full", "short", "good", "yorker", "half-volley", "bouncer", "overpitched"]
lines = ["off-stump", "leg-stump", "middle-stump", "wide", "body-line"]
hit_types = ["inside edge", "outside edge", "top-edge", "bottom-edge", "clean hit", "mishit"]
variations = ["in-swing", "out-swing", "off-cutter", "leg-cutter", "googly", "flipper", "top-spinner", "doosra"]
speeds = ["slow", "medium", "fast", "pace", "spin"]
field_activities = ["catch", "dive", "slide", "stop", "throw", "relay throw", "direct hit", "dropped catch", "misfield",
                    "overthrow"]

# Sample data (replace this with your CSV data later)
commentary_data = [
    "Parag to Madushanka, OUT",
    "Parag to Babar Azam, Four",
    "Saqib Mahmood to Babar Azam, drives through cover for Four",
    "Saqib Mahmood to Babar Azam, short ball, pulled to midwicket for Six",
    "Parag to Babar Azam, full delivery, driven past long-off, no ball"
]

# Function to extract token-level features
def extract_features(token):
    return {
        'text': token.text,
        'lemma': token.lemma_,
        'pos': token.pos_,
        'tag': token.tag_,
        'dep': token.dep_,
        'shape': token.shape_,
        'is_alpha': token.is_alpha,
        'is_stop': token.is_stop,
    }

# Function to label tokens in a commentary
def commentary_to_labels(commentary):
    doc = nlp(commentary)
    labels = []
    bowler = None
    batsman = None

    # Assume the format is "Bowler to Batsman"
    tokens = commentary.split(",")[0].split(" to ")
    if len(tokens) == 2:
        bowler = tokens[0].strip()
        batsman = tokens[1].strip()

    for token in doc:
        token_text = token.text.lower()

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

# Convert commentary to spaCy tokens and extract features
def commentary_to_features(commentary):
    doc = nlp(commentary)
    return [extract_features(token) for token in doc]

# Prepare features and labels for the CRF model
X = [commentary_to_features(comment) for comment in commentary_data]
y = [commentary_to_labels(comment) for comment in commentary_data]

# View the extracted features and labels for a sample commentary
for i, comment in enumerate(commentary_data):
    print(f"Commentary: {comment}")
    print(f"Features: {X[i]}")
    print(f"Labels: {y[i]}")
    print("-" * 50)
