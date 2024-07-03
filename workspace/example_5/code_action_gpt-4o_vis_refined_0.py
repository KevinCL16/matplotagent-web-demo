import matplotlib.pyplot as plt
import numpy as np

# Data for the pie chart
labels = ['Apples', 'Oranges', 'Bananas']
sizes = [35, 45, 20]
explode = (0.1, 0, 0)  # only "explode" the 1st slice (i.e. 'Apples')
colors = ['lightcoral', 'lightskyblue', 'lightgreen']

# Data for the stacked bar chart
age_groups = ['<18', '18-30', '30-50', '50+']
apple_distribution = [25, 40, 20, 15]

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

# Pie chart
wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                                   shadow=True, startangle=140)
ax1.set_title('Fruit Distribution')

# Stacked bar chart
bars = ax2.bar(age_groups, apple_distribution, color='lightcoral', label='Apples')
ax2.set_title('Apples Favorability by Age')
ax2.set_xlabel('Age Groups')
ax2.set_ylabel('Percentage')
ax2.legend()

# Connect the pie chart slice to the bar chart
# Coordinates for the lines
apple_wedge = wedges[0]
theta1, theta2 = apple_wedge.theta1, apple_wedge.theta2
center, r = apple_wedge.center, apple_wedge.r
bar_x = [rect.get_x() + rect.get_width() / 2 for rect in bars]

# Calculate the middle angle of the apple slice
theta = (theta1 + theta2) / 2
x = r * np.cos(np.radians(theta)) + center[0]
y = r * np.sin(np.radians(theta)) + center[1]

# Draw lines
for bx in bar_x:
    ax1.annotate('', xy=(bx, 1), xytext=(x, y),
                 arrowprops=dict(facecolor='black', shrink=0.05, lw=1))

# Adjust layout
plt.subplots_adjust(wspace=0.4)

# Save the plot
plt.savefig('novice_final.png')

# Display the plot
plt.show()