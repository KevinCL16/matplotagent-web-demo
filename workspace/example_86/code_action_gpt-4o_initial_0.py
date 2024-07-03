import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Step 1: Import the necessary libraries
# (Already done above)

# Step 2: Read the CSV file
data = pd.read_csv('data.csv')

# Step 3: Prepare the data
years = data.columns[1:]
windows_versions = data.iloc[:, 0]
market_shares = data.iloc[:, 1:].values

# Calculate the market share of other operating systems
other_os_shares = 100 - market_shares.sum(axis=0)

# Step 4: Set up the doughnut chart
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))

# Define color families for each Windows version
colors = {
    'WinXP': ['#ff9999', '#ff6666', '#ff3333', '#ff0000', '#cc0000'],
    'Win7': ['#99ff99', '#66ff66', '#33ff33', '#00ff00', '#00cc00'],
    'Win8.1': ['#9999ff', '#6666ff', '#3333ff', '#0000ff', '#0000cc'],
    'Win10': ['#ffcc99', '#ff9966', '#ff6633', '#ff3300', '#cc3300']
}

# Create concentric rings for each year
size = 0.3
for i, year in enumerate(years):
    values = list(market_shares[:, i]) + [other_os_shares[i]]
    labels = list(windows_versions) + ['Other OS']
    color_list = [colors[version][i] for version in windows_versions] + ['white']
    
    wedges, texts = ax.pie(values, radius=1 - i*size, colors=color_list, startangle=90, counterclock=False,
                           wedgeprops=dict(width=size, edgecolor='w'))
    
    # Annotate each segment with its market share percentage
    for j, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = (1 - i*size) * 0.5 * (1 + 0.5 * size) * np.sin(np.deg2rad(ang))
        x = (1 - i*size) * 0.5 * (1 + 0.5 * size) * np.cos(np.deg2rad(ang))
        if labels[j] != 'Other OS':
            ax.text(x, y, f"{values[j]:.1f}%", ha='center', va='center', fontsize=8, color='black')

    # Add a white section at the top of each ring to represent other operating systems
    white_patch = patches.Wedge((0, 0), 1 - i*size, 90, 90, width=size, facecolor='white', edgecolor='w')
    ax.add_patch(white_patch)
    ax.text(0, 1 - i*size - size/2, year, ha='center', va='center', fontsize=10, color='black', weight='bold')

# Step 5: Add a legend
legend_labels = [patches.Patch(color=colors[version][0], label=version) for version in windows_versions]
ax.legend(handles=legend_labels, loc='center', bbox_to_anchor=(0.5, 0.5), fontsize=10)

# Step 6: Align the white sections
# (Already ensured by setting startangle=90 and counterclock=False)

# Step 7: Display the chart
plt.title("Desktop Windows Version Market Share Worldwide")
plt.savefig('novice.png')
plt.show()