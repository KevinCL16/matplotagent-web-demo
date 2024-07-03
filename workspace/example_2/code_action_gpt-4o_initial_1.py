import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive plotting
import matplotlib.pyplot as plt
import numpy as np

# Step 2: Create the data
z = np.linspace(-5, 5, 100)
w = np.linspace(-5, 5, 100)

# Step 3: Create the subplots
fig, axs = plt.subplots(3, 3, sharex='col', sharey='row', figsize=(9, 9))
plt.subplots_adjust(wspace=0, hspace=0)  # Step 4: Remove spacing

# Define the plotting data and specifications for each subplot:
plots = [
    (z, w, 'z', 'w'),
    (z**3, w, 'z**3', 'w', 'blue'),
    (-z, w + 1, '-z', 'w + 1', 'yellow'),
    (-z**3, w + 2, '-z**3', 'w + 2', 'purple'),
    (z**2, w**2, 'z**2', 'w**2', 'brown'),
    (-z**2, w**2 + 1, '-z**2', 'w**2 + 1', 'pink'),
    (z**2, -w**2 + 2, 'z**2', '-w**2 + 2', 'grey'),
    (-z**2, -w**2 + 3, '-z**2', '-w**2 + 3', 'black'),
    (z, -w, 'z', '-w', 'white')
]

# Step 5: Plot the data in each subplot
for i, (data_x, data_y, label_x, label_y, *color) in enumerate(plots):
    ax = axs[i // 3, i % 3]
    ax.plot(data_x, data_y, color[0] if color else 'green')  # Default to 'green' if no color specified
    
    # Step 6: Label only the outermost subplots
    if i // 3 < 2:
        ax.tick_params(labelbottom=False)
    if i % 3 > 0:
        ax.tick_params(labelleft=False)

    if i // 3 == 2:
        ax.set_xlabel(label_x)
    if i % 3 == 0:
        ax.set_ylabel(label_y)

# Step 7: Set the overall title
fig.suptitle('Sharing x per column, y per row')

# Step 8: Save the plot to a PNG file
plt.savefig('novice.png')

# Display the plot
plt.show()