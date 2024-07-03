import matplotlib
matplotlib.use('Agg')  # Use Agg backend to avoid GUI requirements
import matplotlib.pyplot as plt
import numpy as np

# Sample data
z = np.linspace(-10, 10, 100)
w = np.linspace(-5, 5, 100)

# Create a 3x3 grid of subplots with shared x-axis per column and y-axis per row
fig, axs = plt.subplots(3, 3, sharex='col', sharey='row', figsize=(10, 10))
fig.suptitle('Sharing x per column, y per row')

# Remove spacing between subplots
plt.subplots_adjust(wspace=0, hspace=0)

# Plot data in each subplot
axs[0, 0].plot(z, w, 'g')
axs[0, 1].plot(z, w**3, 'b')
axs[0, 2].plot(-z, w + 1, 'y')
axs[1, 0].plot(-z**3, w + 2, 'purple')
axs[1, 1].plot(z**2, w**2, 'brown')
axs[1, 2].plot(-z**2, w**2 + 1, 'pink')
axs[2, 0].plot(z**2, -w**2 + 2, 'grey')
axs[2, 1].plot(-z**2, -w**2 + 3, 'black')
axs[2, 2].plot(z, -w, 'white')

# Label only the outermost subplots
for i in range(3):
    for j in range(3):
        if i == 2:
            axs[i, j].set_xlabel(['z', 'z**3', '-z'][j])
        if j == 0:
            axs[i, j].set_ylabel(['w', 'w + 2', '-w**2 + 2'][i])

# Save the plot to a file
plt.savefig("novice_final.png")
plt.show()