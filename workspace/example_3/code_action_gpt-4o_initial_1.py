# Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the backend to Agg for non-GUI environments
plt.switch_backend('Agg')

# Set the seed for reproducibility
np.random.seed(12345678)

# Generate the data
data = [np.sort(np.random.normal(loc=0, scale=std, size=150)) for std in range(2, 7)]

# Calculate the first quartile, median, and third quartile for each array
quartiles = [np.percentile(d, [25, 50, 75]) for d in data]

# Create the subplots
fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(12, 6))

# Plot the default violin plot
sns.violinplot(data=data, ax=axes[0])
axes[0].set_title('Default Violin Plot')

# Plot the customized violin plot
sns.violinplot(data=data, ax=axes[1], inner=None, bw=0.2)
for patch in axes[1].collections:
    patch.set_facecolor('blue')
    patch.set_edgecolor('black')
    patch.set_alpha(0.5)
axes[1].set_title('Customized Violin Plot')

# Customize the first subplot with medians, quartiles, and whiskers
for i, d in enumerate(data):
    q1, med, q3 = quartiles[i]
    axes[0].plot(i, med, 'ro')  # Red dot for the median
    axes[0].vlines(i, q1, q3, colors='black', linestyles='-')  # Vertical lines for the quartiles
    whisker_min = np.percentile(d, 10)  # Assuming whiskers at 10th and 90th percentiles
    whisker_max = np.percentile(d, 90)
    axes[0].vlines(i, whisker_min, whisker_max, colors='black', linestyles='--')  # Whiskers as dashed lines

# Set the x-axis labels for both subplots
for ax in axes:
    ax.set_xticklabels(['E', 'F', 'G', 'H', 'I'])

# Adjust the bottom and wspace of the subplots
plt.subplots_adjust(bottom=0.2, wspace=0.3)

# Save the plot to a file
plt.savefig('novice.png')

# Show the plot
plt.show()