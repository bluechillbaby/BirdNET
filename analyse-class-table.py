import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Read data from CSV file
filePath = './example/test02/'
df = pd.read_csv(filePath + 'result.csv')

# Generate unique colors for each species
unique_species = df['Common Name'].unique()
num_colors = len(unique_species)
colors = plt.cm.tab10(np.linspace(0, 1, num_colors))

# Create a dictionary to map each species to a unique y-value
species_y_values = {species: i for i, species in enumerate(df['Common Name'].unique())}

# Plotting
plt.figure(figsize=(10, 6))
for species, group in df.groupby('Common Name'):
    y_value = species_y_values[species]
    plt.scatter(group['Begin Time (s)'], [y_value]*len(group), s=group['Confidence']*300, label=species, color=colors[y_value], edgecolor='black', linewidth=1, alpha=0.7)
plt.xlabel('Time (s)', weight='bold')
plt.ylabel('Species', weight='bold')
plt.yticks(range(len(species_y_values)), species_y_values.keys())
plt.title('Confidence of Species Detection over Time', weight='bold')
plt.legend()


# Save the plot to a file
plt.savefig(filePath + 'test1.svg')

plt.show()
