import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance

# Load data
data = pd.read_csv('kohli.csv')

# Filter and prepare data
data_filtered = data.dropna(subset=['Line', 'Length', 'Position', 'Runs']).copy()  # Use .copy() to avoid warning
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

# Function to calculate angle separation
# def calculate_angle(coord1, coord2):
#     return np.degrees(np.arctan2(coord2[1], coord2[0]) - np.arctan2(coord1[1], coord1[0]))

# Function to ensure angle separation
def has_equal_angle_separation(selected_positions):
    if len(selected_positions) < 2:  # Need at least two positions to check separation
        return True

    angles = [np.degrees(np.arctan2(y, x)) for x, y in selected_positions]
    angles.sort()
    angle_diff = [abs(angles[i] - angles[i - 1]) for i in range(1, len(angles))]
    angle_diff.append(abs(angles[0] - angles[-1] + 360))  # Wrap-around difference
    return all(abs(d - angle_diff[0]) < 1e-5 for d in angle_diff)  # Check for uniformity

# Function to select positions based on conditions
def select_field_positions(top_positions):
    selected_positions = []
    outside_positions = []
    inside_positions = []
    
    # Select top positions
    for position in top_positions['Position']:
        if position in field_positions:  # Check if the position is valid
            coords = polar_to_cartesian(field_positions[position])
            selected_positions.append((coords, position))
            if coords[0] > 45:  # Outside
                outside_positions.append((coords, position))
            else:  # Inside
                inside_positions.append((coords, position))

    # Ensure at least 2 inside and outside positions
    if len(inside_positions) > 5 and not has_equal_angle_separation([pos[0] for pos in inside_positions]):
        inside_positions = inside_positions[:5]  # Limit to 2 inside positions
    if len(outside_positions) > 2 and not has_equal_angle_separation([pos[0] for pos in outside_positions]):
        outside_positions = outside_positions[:2]  # Limit to 2 outside positions

    selected_positions.extend(inside_positions)
    selected_positions.extend(outside_positions)

    # Fill remaining positions to ensure a total of 9
    while len(selected_positions) < 9:
        for name, coords in field_positions.items():
            if len(selected_positions) >= 9:
                break
            if (coords, name) not in selected_positions:
                selected_positions.append((polar_to_cartesian(coords), name))

    return selected_positions

# Function to plot field setting
def plot_field_setting(line, length):
    line_length = f"{line} - {length}"
    top_positions = percentage_data[percentage_data['Line_Length'] == line_length].sort_values(by='Percentage', ascending=False).head(12)
    
    if top_positions.empty:
        print(f"No data available for Line: {line} and Length: {length}")
        return
    
    #selected_positions = select_field_positions(top_positions)

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

    # # Plot selected fielding positions
    # for (x, y), position in selected_positions:
    #     ax.plot(x, y, 'ro')  # Mark the position with a red dot
    #     ax.text(x, y, f"{position}", ha='center', color="black", fontsize=10)
    i = 0
    for _, row in top_positions.iterrows():
        if i == 10:
            break
        i += 1
        position = row['Position']
        if position in field_positions:
            x, y = polar_to_cartesian(field_positions[position])
            ax.plot(x, y, 'ro')  # Mark the position with a red dot
            ax.text(x, y, f"{position}\n{row['Percentage']:.1f}%", ha='center', color="black", fontsize=10)

    # Plot title and display
    ax.set_title(f"Field Setting Against Kohli for {line} - {length}")
    ax.set_aspect('equal', 'box')
    plt.axis('off')
    plt.show()

# Example usage
plot_field_setting("Outside-off", "Short")