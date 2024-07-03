import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the backend to 'Agg' to avoid GUI-related issues
plt.switch_backend('Agg')

# Step 1: Set the random seed for reproducibility
np.random.seed(12345678)

# Step 2: Generate the data
data = [np.sort(np.random.normal(0, std, 150)) for std in range(2, 7)]

# Step 3: Calculate the first quartile, median, and third quartile
quartiles = [np.percentile(d, [25, 50, 75]) for d in data]

# Step 4: Create the subplots
fig, axes = plt.subplots(1, 2, sharey=True, figsize=(12, 6))

# Step 5: Default violin plot
sns.violinplot(data=data, ax=axes[0])
axes[0].set_xticklabels(['E', 'F', 'G', 'H', 'I'])
axes[0].set_title('Default Violin Plot')

# Step 6: Customized violin plot
sns.violinplot(data=data, ax=axes[1], inner=None, color='blue', linewidth=1.5, alpha=0.5)
for violin in axes[1].collections:
    violin.set_edgecolor('black')
axes[1].set_xticklabels(['E', 'F', 'G', 'H', 'I'])
axes[1].set_title('Customized Violin Plot')

# Step 7: Plot medians, quartiles, and whiskers on the first subplot
for i, q in enumerate(quartiles):
    # Plot median
    axes[0].scatter(i, q[1], color='red', zorder=3)
    # Plot quartiles
    axes[0].vlines(i, q[0], q[2], color='black', linestyle='-', lw=2)
    # Plot whiskers
    whisker_low = np.percentile(data[i], 10)
    whisker_high = np.percentile(data[i], 90)
    axes[0].vlines(i, whisker_low, whisker_high, color='black', linestyle='--', lw=1)

# Step 8: Adjust the layout
plt.subplots_adjust(bottom=0.2, wspace=0.3)

# Save the plot to a file
plt.savefig("novice.png")

# Show the plot
plt.show()