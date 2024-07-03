import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the seed for reproducibility
np.random.seed(12345678)

# Generate data
data = [np.sort(np.random.normal(0, std, 150)) for std in range(2, 7)]

# Create subplots
fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(12, 6))

# First subplot: Default violin plot
sns.violinplot(data=data, ax=axes[0])
axes[0].set_title('Default Violin Plot')

# Calculate quartiles and medians
quartiles = [np.percentile(d, [25, 50, 75]) for d in data]
whiskers = [np.percentile(d, [5, 95]) for d in data]

# Plot medians, quartiles, and whiskers
for i, (q, w) in enumerate(zip(quartiles, whiskers)):
    axes[0].plot(i, q[1], 'ro')  # Median
    axes[0].vlines(i, q[0], q[2], color='k', linestyle='-')  # Quartiles
    axes[0].vlines(i, w[0], w[1], color='k', linestyle='--')  # Whiskers

# Second subplot: Customized violin plot
sns.violinplot(data=data, ax=axes[1], inner=None, color='blue', linewidth=1, alpha=0.5)
axes[1].set_title('Customized Violin Plot')

# Set x-axis labels
for ax in axes:
    ax.set_xticklabels(['E', 'F', 'G', 'H', 'I'])

# Adjust layout
plt.subplots_adjust(bottom=0.2, wspace=0.3)

# Save the plot
plt.savefig("novice_final.png")

# Show the plot
plt.show()