import pandas as pd
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Load and Prepare Data
# Read data from CSV
data = pd.read_csv('data.csv')

# Exclude the first column (gene identifiers) and transpose the matrix
data_transposed = data.iloc[:, 1:].transpose()

# Step 2: Hierarchical Clustering
# Calculate pairwise correlation matrix
correlation_matrix = data_transposed.corr()

# Perform hierarchical clustering
Z = hierarchy.linkage(correlation_matrix, method='average')

# Step 3: Circular Dendrogram Transformation and Plotting
# Convert dendrogram coordinates to circular format
def dendrogram_coord_convert(Z):
    dendro = hierarchy.dendrogram(Z, no_plot=True)
    icoord = np.array(dendro['icoord'])
    dcoord = np.array(dendro['dcoord'])
    
    # Adjust the coordinates to fit in a polar plot
    theta = []
    radius = []
    for xs, ys in zip(icoord, dcoord):
        for x, y in zip(xs, ys):
            theta.append(np.deg2rad(x))
            radius.append(y)
    return np.array(theta), np.array(radius)

theta, radius = dendrogram_coord_convert(Z)

# Step 4: Enhancement and Annotation
# Example of color-coding by clusters (can be adjusted based on actual clustering results)
cutree = hierarchy.cut_tree(Z, n_clusters=4).flatten()  # Example clustering result

# Plot with color-coded clusters
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
for cluster in np.unique(cutree):
    mask = (cutree == cluster)
    ax.scatter(theta[mask], radius[mask], label=f'Cluster {cluster + 1}', s=10)  # Adjusted the size for better visibility

# Label tissue samples at the perimeter
perimeter_labels = list(data.columns[1:])
perimeter_angles = np.linspace(0, 2 * np.pi, len(perimeter_labels), endpoint=False)
for angle, label in zip(perimeter_angles, perimeter_labels):
    ax.text(angle, ax.get_ylim()[1] + 0.1, label, ha='center', va='center', fontsize=8)  # Adjusted fontsize for better visibility

# Design a correlation axis (not implemented in this example)

ax.set_title('Circular Dendrogram with Clusters', va='bottom')
ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

# Save the plot to a file
plt.savefig('novice.png')
plt.show()