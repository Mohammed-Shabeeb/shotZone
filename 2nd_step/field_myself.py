import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    "Forward-square-leg": (45, 365), 
    "Mid-wicket": (45, 345), 
    "Deep-mid-wicket": (85, 345),
    "Mid-on": (30, 300), 
    "Long-on": (85, 290), 
    "Fine-leg": (70, 60), 
    "Short-fine-leg": (50, 60),
    "Backward-short-leg": (35, 55), 
    "Straight-hit": (85, 270), 
    "Third-man": (70, 115),
    "Deep-backward-point": (85, 160), 
    "Deep-cover-point": (85, 185), 
    "Long-stop": (85, 90),
    "Deep-fine-leg": (85, 55), 
    "Deep-square-leg": (85, 365),
    "Cow-corner": (85, 315),
    "Deep-cover": (85, 195),
    "Deep-point": (85, 175),
    "Deep-square": (85, 35),
    "Deep-third": (85, 120),
    "Long-leg": (85, 75),
    "Midwicket": (45, 345),
    "Second-slip": (15, 107.5),
    "Short-leg": (10, 35),
    "Short-third-man": (50, 115),
    "Silly-mid-off": (5, 175),
    "Silly-mid-on": (5, 365), 
    "Silly-point": (10, 145)
}

# Convert polar coordinates to Cartesian coordinates
def polar_to_cartesian(polar_coords):
    distance, angle = polar_coords
    angle_rad = np.radians(angle)
    x = distance * np.cos(angle_rad)
    y = distance * np.sin(angle_rad)
    return x, y

# Function to draw region boundaries
def draw_region_boundaries(ax, regions):
    for (start_angle, end_angle), region_id in regions.items():
        # Convert polar to Cartesian coordinates
        start_rad = np.radians(start_angle)
        end_rad = np.radians(end_angle)
        
        # Draw the lines for each boundary
        x_start = 100 * np.cos(start_rad)
        y_start = 100 * np.sin(start_rad)
        x_end = 100 * np.cos(end_rad)
        y_end = 100 * np.sin(end_rad)

        # Draw the boundary line
        ax.plot([0, x_start], [0, y_start], color='black', linestyle='-', linewidth=2)
        ax.plot([0, x_end], [0, y_end], color='black', linestyle='-', linewidth=2)

        # Label the region in the middle
        mid_angle = (start_angle + end_angle) / 2
        mid_rad = np.radians(mid_angle)
        x_mid = 75 * np.cos(mid_rad)
        y_mid = 75 * np.sin(mid_rad)
        ax.text(x_mid, y_mid, str(region_id), fontsize=12, ha='center', va='center')


# Function to plot field setting using both insights
def plot_field_setting(line, length):
    line_length = f"{line} - {length}"
    top_positions = percentage_data[percentage_data['Line_Length'] == line_length].sort_values(by='Percentage', ascending=False)

    if top_positions.empty:
        print(f"No data available for Line: {line} and Length: {length}")
        return
    
    # Print top field positions to console
    print("Top Field Positions:")
    for _, row in top_positions.iterrows():
        print(f"  Position: {row['Position']} - Percentage: {row['Percentage']:.2f}%")

    # Get average runs for this line-length combination
    avg_runs = combination_stats[(combination_stats['Line'] == line) & (combination_stats['Length'] == length)]['Average_Runs']
    avg_runs = avg_runs.values[0] if not avg_runs.empty else "No data"
    
    # Create the cricket field
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

    #partition ground into different regions
    regions = {
       (54, 126): 1, (126, 174): 2, (174, 222): 3, (222, 270): 4, (270, 318): 5, (318, 366): 6, (6, 54): 7
    }


    # Draw region boundaries
    draw_region_boundaries(ax, regions)


    #to count selected positions from each region
    regions_count = dict((i, 0) for i in range(1, 8))
    
    selected_positions = []
    for _, row in top_positions.iterrows():
        position = row['Position']
        if position in field_positions:
            x, y = polar_to_cartesian(field_positions[position])
            angle = y
            if angle < 54:
                region = 7
            elif angle < 126:
                region = 1
            elif angle < 174:
                region = 2
            elif angle < 222:
                region = 3
            elif angle < 270:
                region = 4
            elif angle < 318:
                region = 5
            else:
                region = 6

            if regions_count[region] < 2:
                #ax.plot(x, y, 'ro')  # Mark the position with a red dot
                #ax.text(x, y, f"{position}\n{row['Percentage']:.1f}%", ha='center', color="black", fontsize=10)
                regions_count[region] += 1
                selected_positions.append(position)
                if len(selected_positions) > 9:
                    break

    for position, value in field_positions.items():
        if position not in selected_positions:
            x, y = value
            
            angle = y
            if angle < 54:
                region = 7
            elif angle < 126:
                region = 1
            elif angle < 174:
                region = 2
            elif angle < 222:
                region = 3
            elif angle < 270:
                region = 4
            elif angle < 318:
                region = 5
            else:
                region = 6

            if regions_count[region] < 2:
                regions_count[region] += 1
                selected_positions.append(position)
                if len(selected_positions) > 9:
                    break

    print(regions_count)
    print(selected_positions)

    for position in selected_positions:
        x, y = polar_to_cartesian(field_positions[position])
        ax.plot(x, y, 'ro')  # Mark the position with a red dot
        ax.text(x, y, f"{position}\n{row['Percentage']:.1f}%", ha='center', color="black", fontsize=10)
    

    
    

    # Plot the top fielding positions based on the printed output
    print(f"Number of top positions: {len(top_positions)}")  # Debugging line
    # for _, row in top_positions.iterrows():
    #     position = row['Position']
    #     if position in field_positions:
    #         x, y = polar_to_cartesian(field_positions[position])
    #         ax.plot(x, y, 'ro')  # Mark the position with a red dot
    #         ax.text(x, y, f"{position}\n{row['Percentage']:.1f}%", ha='center', color="black", fontsize=10)
    
    # Set plot details
    ax.set_title(f"Field Setting for {line} - {length} | Avg Runs: {avg_runs:.1f}")
    ax.set_aspect('equal', 'box')
    plt.axis('off')  # Hide axis
    plt.show()

# Example usage
plot_field_setting("Outside-off", "Good")
