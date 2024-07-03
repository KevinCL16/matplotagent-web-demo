import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Step 1: Generate the correlated dataset
mean = [4, 3.5]
cov = [[0.6, 0.85], [-0.3, 0.25]]  # Covariance matrix
data = np.random.multivariate_normal(mean, cov, 700)

# Step 2: Create the scatter plot
plt.figure(figsize=(6, 6))
plt.scatter(data[:, 0], data[:, 1], s=10, alpha=0.5)

# Step 3: Add vertical and horizontal lines
plt.axvline(x=mean[0], color='grey', linestyle='--')
plt.axhline(y=mean[1], color='grey', linestyle='--')

# Step 4: Function to plot confidence ellipses
def plot_confidence_ellipse(ax, mean, cov, n_std, facecolor='none', edgecolor='black', linestyle='-'):
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2, facecolor=facecolor, edgecolor=edgecolor, linestyle=linestyle)
    scale_x = np.sqrt(cov[0, 0]) * n_std
    scale_y = np.sqrt(cov[1, 1]) * n_std
    transf = plt.transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(mean[0], mean[1])
    ellipse.set_transform(transf + ax.transData)
    ax.add_patch(ellipse)

# Step 5: Overlay confidence ellipses
ax = plt.gca()
plot_confidence_ellipse(ax, mean, cov, 1, edgecolor='firebrick', linestyle='-')
plot_confidence_ellipse(ax, mean, cov, 2, edgecolor='fuchsia', linestyle='--')
plot_confidence_ellipse(ax, mean, cov, 3, edgecolor='blue', linestyle=':')

# Step 6: Highlight a specific point
plt.plot(1, 1, 'ro', label='Point (1, 1)')

# Step 7: Add title and legend
plt.title('Different standard deviations')
plt.legend(['$1\sigma$', '$2\sigma$', '$3\sigma$', 'Point (1, 1)'])

# Step 8: Save the plot to a file
plt.savefig('novice.png')

# Display the plot
plt.show()