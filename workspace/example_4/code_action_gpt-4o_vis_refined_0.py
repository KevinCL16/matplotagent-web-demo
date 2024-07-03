import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

# Generate the correlated dataset
np.random.seed(0)
mean = [4, 3.5]
cov = [[0.6, 0.85], [-0.3, 0.25]]
x, y = np.random.multivariate_normal(mean, cov, 700).T

# Create the plot
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(x, y, s=10)

# Add vertical and horizontal lines
ax.axhline(y=mean[1], color='grey', linestyle='--')
ax.axvline(x=mean[0], color='grey', linestyle='--')

# Function to draw ellipses
def confidence_ellipse(x, y, ax, n_std=1.0, facecolor='none', **kwargs):
    if x.size != y.size:
        raise ValueError("x and y must be the same size")
    
    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2, facecolor=facecolor, **kwargs)
    
    scale_x = np.sqrt(cov[0, 0]) * n_std
    scale_y = np.sqrt(cov[1, 1]) * n_std
    transf = transforms.Affine2D().rotate_deg(180 * np.arcsin(pearson) / np.pi).scale(scale_x, scale_y).translate(np.mean(x), np.mean(y))
    
    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

# Overlay confidence ellipses
confidence_ellipse(x, y, ax, n_std=1, edgecolor='firebrick', label='$1\sigma$')
confidence_ellipse(x, y, ax, n_std=2, edgecolor='fuchsia', linestyle='--', label='$2\sigma$')
confidence_ellipse(x, y, ax, n_std=3, edgecolor='blue', linestyle=':', label='$3\sigma$')

# Highlight the specific point
ax.plot(1, 1, 'ro', label='Point (1, 1)')

# Add title and legend
ax.set_title('Different Standard Deviations')
ax.legend()

# Save the plot
plt.savefig('novice_final.png')
plt.show()