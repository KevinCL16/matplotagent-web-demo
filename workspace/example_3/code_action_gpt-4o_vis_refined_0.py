import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the seed for reproducibility
np.random.seed(12345678)

# Generate data
data = [np.sort(np.random.normal(0, std, 150)) for std in range(2, 7)]

# Create subplots
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)

# Default violin plot
sns.violinplot(data=data, ax=ax1)
ax1.set_title('Default Violin Plot')

# Calculate quartiles and medians
quartiles = [np.percentile(d, [25, 50, 75]) for d in data]
whiskers = [(np.min(d), np.max(d)) for d in data]

# Plot medians, quartiles, and whiskers
for i, (q, w) in enumerate(zip(quartiles, whiskers)):
    ax1.plot(i, q[1], 'ro')  # Median
    ax1.vlines(i, q[0], q[2], colors='k', linestyles='-')  # Quartiles
    ax1.vlines(i, w[0], w[1], colors='k', linestyles='--')  # Whiskers

# Customized violin plot
sns.violinplot(data=data, ax=ax2, inner=None, color='blue', linewidth=1, alpha=0.5)
ax2.set_title('Customized Violin Plot')

# Set x-axis labels
labels = ['E', 'F', 'G', 'H', 'I']
ax1.set_xticklabels(labels)
ax2.set_xticklabels(labels)

# Adjust layout
plt.subplots_adjust(bottom=0.2, wspace=0.3)

# Save the plot
plt.savefig("novice_final.png")

# Show the plot
plt.show()