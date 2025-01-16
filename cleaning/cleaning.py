import pandas as pd
import re

# Load the data
file_path = '../16_1_2025/in/merged.csv'
df = pd.read_csv(file_path)

# Convert 'commentary' and 'second_commentary' columns to lowercase
df['commentary'] = df['commentary'].str.lower()
df['second_commentary'] = df['second_commentary'].str.lower()

# Append "long-stop" to the 'commentary' column only if the score is "4lb"
df.loc[df['score'] == "4lb", 'commentary'] += " long-stop"

# Replace phrases that match the pattern "between [something] and mid off/on" with "straight-hit"
df['commentary'] = df['commentary'].str.replace(r'between\s+\w+\s+and\s+mid\s+off', 'straight-hit', regex=True)
df['commentary'] = df['commentary'].str.replace(r'between\s+\w+\s+and\s+mid\s+on', 'straight-hit', regex=True)
df['commentary'] = df['commentary'].str.replace(r'between\s+mid\s+off\s+and\s+\w+', 'straight-hit', regex=True)
df['commentary'] = df['commentary'].str.replace(r'between\s+mid\s+on\s+and\s+\w+', 'straight-hit', regex=True)

df['second_commentary'] = df['second_commentary'].str.replace(r'between\s+\w+\s+and\s+mid\s+off', 'straight-hit', regex=True)
df['second_commentary'] = df['second_commentary'].str.replace(r'between\s+\w+\s+and\s+mid\s+on', 'straight-hit', regex=True)
df['second_commentary'] = df['second_commentary'].str.replace(r'between\s+mid\s+off\s+and\s+\w+', 'straight-hit', regex=True)
df['second_commentary'] = df['second_commentary'].str.replace(r'between\s+mid\s+on\s+and\s+\w+', 'straight-hit', regex=True)


# Replace '(' and ')' with spaces, and replace 's only where it occurs after an apostrophe
df['commentary'] = df['commentary'].str.replace(r"[()!.]", ' ', regex=True)
df['commentary'] = df['commentary'].str.replace(r"'s\b", ' ', regex=True)  # Only replaces 's
df['second_commentary'] = df['second_commentary'].str.replace(r"[()!.]", ' ', regex=True)
df['second_commentary'] = df['second_commentary'].str.replace(r"'s\b", ' ', regex=True)  # Only replaces 's

# Replace ',' with ' ,'
df['commentary'] = df['commentary'].str.replace(r",", ' ,', regex=True)
df['second_commentary'] = df['second_commentary'].str.replace(r",", ' ,', regex=True)

# Replace back of a length with good
df['commentary'] = df['commentary'].str.replace(r"\bback of a length\b", 'good', regex=True)
df['second_commentary'] = df['second_commentary'].str.replace(r"\bback of a length\b", 'good', regex=True)

#replacement for lines
#lines = ["off-stump", "leg-stump", "middle-stump", "body-line", "fourth stump", "fifth stump"]
off_lines = ["off-stump", "off stump" "fourth stump", "fifth stump", "outside off", "plays through the line", "guided down to third man",
             "driven through cover", "cut away past point", "nips back in towards off", "lofted over long-off",
             "steers it to backward point", "defends off the front foot", "over long-off", "full on off",
             "full and not quite in the blockhole"]
leg_lines = ["leg-stump", "leg stump", "body-line", "body line", "on middle and leg", "clipped off his pads",
             "worked through square leg", "glanced down to fine leg", "drifting down leg", 
             "angling down leg side", "slog-swept to deep square leg", "pulled to deep mid-wicket", "flicked off his pads",
             "swatted flat over deep midwicket", "slower ball sits in the pitch", "pull into the leg-side", "pulled to leg-side"
               ]
middle_lines = ["middle-stump", "middle stump", "on off and middle", "full on middle", "plays straight through the line",
                "defended back to the bowler", "punches down the ground", "nips back in towards middle", "seaming in on middle",
                "pushed back to mid-on", "works it to mid-wicket"]

def replace_line_patterns(df, column, patterns, replacement):
    for pattern in patterns:
        df[column] = df[column].str.replace(rf'\b{pattern}\b', replacement, regex=True)

# Apply replacements
replace_line_patterns(df, 'commentary', off_lines, "outside-off")
replace_line_patterns(df, 'commentary', leg_lines, "leg-stump")
replace_line_patterns(df, 'commentary', middle_lines, "middle-stump")
replace_line_patterns(df, 'second_commentary', off_lines, "outside-off")
replace_line_patterns(df, 'second_commentary', leg_lines, "leg-stump")
replace_line_patterns(df, 'second_commentary', middle_lines, "middle-stump")





# List of shot types and positions
shot_types = [
    "reverse sweep", "upper cut", "straight drive", "cover drive", "on drive", "off drive", "defensive shot", "square drive",
    "cut shot", "pull shot", "hook shot", "backfoot defence", "square cut", "scoop shot", "ramp shot", "flick shot"
]

shot_positions = [
    "second slip", "fly slip", "short third man", "backward point", "deep point",
    "deep backward point", "extra cover", "deep cover", "deep extra cover", "mid-off", "long off",
    "straight hit", "mid-on", "long on", "cow corner", "deep mid-wicket", "midwicket", "short leg", "silly mid-off",
    "silly mid-on", "silly point", "short fine leg", "fine leg", "deep fine leg", "long leg", "backward square leg",
    "square leg", "leg gully", "third man", "long stop", "deep square", "leg side", "deep square leg", "on side", "off side", "deep mid-on"
    "cover point", "deep third"
]



hit_types = ["clean hit", "inside edge", "outside edge", "thick edge", "thin edge", "miss hit"]

variations = ["carrom ball"]

field_activities = ["relay throw", "direct hit", "dropped catch", "run out", "hit wicket", "leg before wicket",
                    "fielding error", "miss field"]

# Create dictionaries for two-word items with hyphenated replacements
hyphenated_shots = {shot: shot.replace(" ", "-") for shot in shot_types if " " in shot}
hyphenated_positions = {position: position.replace(" ", "-") for position in shot_positions if " " in position}
#hyphenated_lines = {line: line.replace(" ", "-") for line in lines if " " in line}
hyphenated_hits = {hit: hit.replace(" ", "-") for hit in hit_types if " " in hit}
hyphenated_variations = {variation: variation.replace(" ", "-") for variation in variations if " " in variation}
hyphenated_fields = {field: field.replace(" ", "-") for field in field_activities if " " in field}

# Function to replace two-wvariations and positions with hyphenated versions
def hyphenate_terms(text):
    for shot, hyphenated_shot in hyphenated_shots.items():
        text = re.sub(rf'\b{shot}\b', hyphenated_shot, text)
    for position, hyphenated_position in hyphenated_positions.items():
        text = re.sub(rf'\b{position}\b', hyphenated_position, text)
    #for line, hyphenated_line in hyphenated_lines.items():
    #    text = re.sub(rf'\b{line}\b', hyphenated_line, text)
    for hit, hyphenated_hit in hyphenated_hits.items():
        text = re.sub(rf'\b{hit}\b', hyphenated_hit, text)
    for variation, hyphenated_variation in hyphenated_variations.items():
        text = re.sub(rf'\b{variation}\b', hyphenated_variation, text)
    for field, hyphenated_field in hyphenated_fields.items():
        text = re.sub(rf'\b{field}\b', hyphenated_field, text)
    return text

# Apply the function to both commentary columns
df['commentary'] = df['commentary'].apply(hyphenate_terms)
df['second_commentary'] = df['second_commentary'].apply(hyphenate_terms)

# Save the cleaned data to a new CSV file
updated_file_path = '../16_1_2025/out/pbks_rcb_25_march_2025_rcb_batting.csv'
df.to_csv(updated_file_path, index=False)
print("file saved to", updated_file_path)
