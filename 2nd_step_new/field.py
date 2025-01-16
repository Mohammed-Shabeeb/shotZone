import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance

# Load data
data = pd.read_csv('kohli_overs_6_to_15.csv')

# Filter and prepare data
data_filtered = data.dropna(subset=['Line', 'Length', 'Position', 'Runs'])
data_filtered['Line_Length'] = data_filtered['Line'] + " - " + data_filtered['Length']
combination_counts = data_filtered.groupby(['Line_Length', 'Position']).size().reset_index(name='Count')
total_counts = data_filtered.groupby('Line_Length').size().reset_index(name='Total')
percentage_data = combination_counts.merge(total_counts, on='Line_Length')
percentage_data['Percentage'] = (percentage_data['Count'] / percentage_data['Total']) * 100

# Calculate average runs for each line-length combination
combination_stats = data_filtered.groupby(['Line', 'Length']).agg({'Runs': 'sum', 'Position': 'count'}).reset_index()
combination_stats.columns = ['Line', 'Length', 'Total_Runs', 'Count']
combination_stats['Average_Runs'] = combination_stats['Total_Runs'] / combination_stats['Count']

# Field positions in polar coordinates (distance in meters, angle in degrees)
field_positions = {
    "Slip": (15, 105), 
    "Gully": (30, 150), 
    "Point": (45, 170), 
    "Backward-point": (45, 160),
    "Cover-point": (45, 180), 
    "Cover": (45, 195), 
    "Extra-cover": (45, 210), 
    "Deep-extra-cover": (85, 210),
    "Mid-off": (30, 240), 
    "Long-off": (85, 250), 
    "Fly-slip": (30, 120), 
    "Leg-slip": (15, 70),
    "Leg-gully": (30, 30), 
    "Square-leg": (45, 10), 
    "Backward-square-leg": (45, 20),
    "Forward-square-leg": (45, 5), 
    "Mid-wicket": (45, -15), 
    "Deep-mid-wicket": (85, -15),
    "Mid-on": (30, -60), 
    "Long-on": (85, -70), 
    "Fine-leg": (70, 60), 
    "Short-fine-leg": (50, 60),
    "Backward-short-leg": (35, 55), 
    "Straight-hit": (85, -90), 
    "Third-man": (70, 115),
    "Deep-backward-point": (85, 160), 
    "Deep-cover-point": (85, 185), 
    "Long-stop": (85, 90),
    "Deep-fine-leg": (85, 55), 
    "Deep-square-leg": (85, 5),
    "Cow-corner": (85, -45),
    "Deep-cover": (85, 195),
    "Deep-point": (85, 175),
    "Deep-square": (85, 35),
    "Deep-third": (85, 120),
    "Long-leg": (85, 75),
    "Midwicket": (45, -15),
    "Second-slip": (15, 107.5),
    "Short-leg": (10, 35),
    "Short-third-man": (50, 115),
    "Silly-mid-off": (5, 175),
    "Silly-mid-on": (5, 5), 
    "Silly-point": (10, 145)
}

# Convert polar coordinates to Cartesian coordinates
def polar_to_cartesian(polar_coords):
    distance, angle = polar_coords
    angle_rad = np.radians(angle)
    x = distance * np.cos(angle_rad)
    y = distance * np.sin(angle_rad)
    return x, y

# Function to eliminate closely located positions
def eliminate_nearby_positions(positions, threshold_distance=30):
    final_positions = []
    for pos in positions:
        if all(distance.euclidean(pos[1], other[1]) > threshold_distance for other in final_positions):
            final_positions.append(pos)
    return final_positions

# Function to ensure angle separation
def make_angle_separation(positions):
    if not positions:
        return []
    
    angles = np.array([np.arctan2(y, x) for _, (x, y) in positions])
    sorted_indices = np.argsort(angles)
    sorted_positions = [positions[i] for i in sorted_indices]

    unique_positions = []
    for i, pos in enumerate(sorted_positions):
        if i == 0 or i == len(sorted_positions) - 1 or np.abs(angles[sorted_indices[i]] - angles[sorted_indices[i - 1]]) > np.pi / len(positions):
            unique_positions.append(pos)
    return unique_positions

# Function to add extra positions for coverage if needed
def add_extra_positions(selected_positions, all_positions, max_positions=9):
    selected_names = {pos[0] for pos in selected_positions}
    for name, coords in all_positions:
        if name not in selected_names:
            selected_positions.append((name, coords))
        if len(selected_positions) >= max_positions:
            break
    return selected_positions

# Function to categorize positions into inside and outside
def categorize_positions(positions):
    inside_positions = []
    outside_positions = []
    for pos in positions:
        distance_value = pos[1][0]
        if distance_value <= 55:
            inside_positions.append(pos)
        else:
            outside_positions.append(pos)
    return inside_positions, outside_positions

# Function to plot field setting
def plot_field_setting(line, length):
    line_length = f"{line} - {length}"
    top_positions = percentage_data[percentage_data['Line_Length'] == line_length].sort_values(by='Percentage', ascending=False)

    if top_positions.empty:
        print(f"No data available for Line: {line} and Length: {length}")
        return

    print("Top Field Positions (Filtered):")
    top_positions = top_positions.head(12)  # Get extra positions to filter for overlap
    positions_with_coords = [(row['Position'], polar_to_cartesian(field_positions[row['Position']])) 
                             for _, row in top_positions.iterrows() if row['Position'] in field_positions]

    # Filter out closely located positions
    filtered_positions = eliminate_nearby_positions(positions_with_coords)

    # Categorize positions into inside and outside
    inside_positions, outside_positions = categorize_positions(filtered_positions)

    # Select positions ensuring angular separation
    inside_selected = make_angle_separation(inside_positions)
    outside_selected = make_angle_separation(outside_positions)

    # Ensure at least two positions from the top 4
    selected_top_positions = positions_with_coords[:4]  # Top 4 positions
    top_selected = []
    
    # Add at least 2 top positions if they are not already included
    for pos in selected_top_positions:
        if pos not in inside_selected and pos not in outside_selected:
            top_selected.append(pos)

    # Keep only 2 top positions
    top_selected = top_selected[:2]

    # Combine all selected positions while ensuring a maximum of 9
    final_positions = inside_selected + outside_selected + top_selected
    final_positions = eliminate_nearby_positions(final_positions)[:9]  # Ensure we only keep 9 positions

    # If less than 9 positions, add more from remaining
    if len(final_positions) < 9:
        remaining_positions = [pos for pos in filtered_positions if pos not in final_positions]
        final_positions.extend(remaining_positions[:(9 - len(final_positions))])  # Fill up to 9

    # Ensure only 9 positions total
    final_positions = final_positions[:9]

    for position, (x, y) in final_positions:
        percentage = top_positions[top_positions['Position'] == position]['Percentage'].values[0] if position in top_positions['Position'].values else 0
        print(f"  Position: {position} - Percentage: {percentage:.2f}%")

    # Create plot for field setting
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)

    # Draw circles representing the field
    for radius in [45, 90]:
        circle = plt.Circle((0, 0), radius, color="green", fill=False, linestyle="--")
        ax.add_artist(circle)

    # Draw the pitch (rotated 90 degrees counterclockwise)
    pitch = plt.Rectangle((-4, -10), 8, 20, color="brown")
    ax.add_artist(pitch)

    # Add keeper position
    keeper_x, keeper_y = polar_to_cartesian((20, 90))
    ax.plot(keeper_x, keeper_y, 'bo', label="Keeper")  # Keeper position in blue
    ax.text(keeper_x, keeper_y, "Keeper", ha='center', color="blue", fontsize=10)

    # Plot selected fielding positions
    for position, (x, y) in final_positions:
        ax.plot(x, y, 'ro')  # Mark the position with a red dot
        ax.text(x, y, f"{position}", ha='center', color="black", fontsize=10)

    # Plot title and display
    ax.set_title(f"Field Setting for {line} - {length}")
    ax.set_aspect('equal', 'box')
    plt.axis('off')
    plt.show()

# Example usage
plot_field_setting("Outside-off", "Good")
