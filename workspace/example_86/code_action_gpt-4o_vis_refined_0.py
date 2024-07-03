import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = pd.read_csv('data.csv')

# Extract the years and Windows versions
years = data.columns[1:]
windows_versions = data.iloc[:, 0]

# Define colors for each Windows version
colors = {
    'WinXP': ['#ff9999','#ff6666','#ff3333','#ff0000','#cc0000'],
    'Win7': ['#66b3ff','#3399ff','#0073e6','#0059b3','#004080'],
    'Win8.1': ['#99ff99','#66ff66','#33cc33','#00b300','#008000'],
    'Win10': ['#ffcc99','#ff9966','#ff6600','#cc5200','#993d00']
}

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))

# Initialize the size of the white section
white_section_size = 0.1

# Initialize the size of the rings
size = 0.3

# Initialize the starting angle for the white section
startangle = 90

# Plot each year as a concentric ring
for i, year in enumerate(years):
    # Extract the market share data for the year
    market_share = data[year]
    
    # Add the white section for other operating systems
    market_share = np.append(market_share, white_section_size * 100)
    
    # Define the colors for the segments
    ring_colors = [colors[windows_versions[j]][i] for j in range(len(windows_versions))] + ['white']
    
    # Plot the ring
    wedges, texts, autotexts = ax.pie(market_share, radius=1 - i * size, colors=ring_colors,
                                      startangle=startangle, counterclock=False,
                                      wedgeprops=dict(width=size, edgecolor='w'),
                                      autopct='%1.1f%%', pctdistance=0.85)
    
    # Annotate each segment with its respective market share percentage
    for j, autotext in enumerate(autotexts):
        if j < len(windows_versions):
            autotext.set_text(f'{market_share[j]:.1f}%')
        else:
            autotext.set_text('')

    # Annotate the white section with the year
    ax.text(0, 1 - i * size - size / 2, year, ha='center', va='center', color='black', fontsize=12, fontweight='bold')

# Add a legend in the center
legend_labels = [f'{version}' for version in windows_versions]
legend_colors = [colors[version][2] for version in windows_versions]
ax.legend(legend_labels, loc='center', frameon=False, fontsize=12, bbox_to_anchor=(0.5, 0.5))

# Set the title
plt.title('Desktop Windows Version Market Share Worldwide', fontsize=16)

# Save the plot
plt.savefig('novice_final.png', bbox_inches='tight')

# Show the plot
plt.show()