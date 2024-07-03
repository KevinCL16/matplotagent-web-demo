import matplotlib.pyplot as plt

# Step 2: Prepare Data for the Pie Chart
labels_pie = ['Apples', 'Oranges', 'Bananas']
sizes_pie = [35, 45, 20]
explode_pie = (0.1, 0, 0)  # To separate the 'Apples' slice

# Step 4: Prepare Data for the Stacked Bar Chart
labels_bar = ['<18', '18-30', '30-50', '50+']
percentages_apples = [25, 40, 20, 15]
percentages_oranges = [30, 35, 25, 10]
percentages_bananas = [45, 25, 20, 10]

# Calculate cumulative percentages for stacked bar chart
bottom_oranges = percentages_apples
bottom_bananas = [x + y for x, y in zip(percentages_apples, percentages_oranges)]

# Step 3 & 5: Create the Pie Chart and Stacked Bar Chart
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

# Pie chart
ax1.pie(sizes_pie, explode=explode_pie, labels=labels_pie, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99'])
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
ax1.set_title('Fruit Distribution')

# Stacked bar chart
ax2.bar(labels_bar, percentages_apples, color='#ff9999', label='Apples')
ax2.bar(labels_bar, percentages_oranges, bottom=bottom_oranges, color='#66b3ff', label='Oranges')
ax2.bar(labels_bar, percentages_bananas, bottom=bottom_bananas, color='#99ff99', label='Bananas')

# Add legend
ax2.legend(loc='upper left')

# Set labels and title
ax2.set_ylabel('Percentage')
ax2.set_xlabel('Age Groups')
ax2.set_title('Apples Favorability by Age')

# Adjust layout
plt.tight_layout()

# Save plot to file
plt.savefig('novice.png')

# Display plot
plt.show()