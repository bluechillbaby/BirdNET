import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define frequency ranges
high_freq_species = {
    'Superb Fairywren': (4000, 8000),
    'Variegated Fairywren': (4000, 8000),
    'Splendid Fairywren': (4000, 8000),
    'White-Winged Fairywren': (4000, 8000),
    'Purple-backed Fairywren': (4000, 8000)
}

low_freq_species = {
    'Laughing Kookaburra': (300, 3000),
    'Brolga': (100, 2000),
    'Tawny Frogmouth': (100, 4000)
}

# Define colors for each species
species_colors = {
    'Superb Fairywren': 'blue',
    'Variegated Fairywren': 'green',
    'Splendid Fairywren': 'red',
    'White-winged Fairywren': 'orange',
    'White-Winged Fairywren': 'orange',
    'Purple-backed Fairywren': 'purple',
    'Laughing Kookaburra': 'blue',
    'Brolga': 'green',
    'Tawny Frogmouth': 'orange'
}

### Plotting frequency bars

# Plotting
plt.figure(figsize=(12, 8))  # Increase figure size

# Plot high frequency range species
for i, (species, freq_range) in enumerate(high_freq_species.items()):
    color = species_colors.get(species)  # Get species color from species_colors dictionary
    plt.barh(i, freq_range[1] - freq_range[0], left=freq_range[0], color=color, alpha=0.5, label='High Frequency Range')
    plt.text(freq_range[0], i, str(freq_range[0]), ha='right', va='center', color='black')
    plt.text(freq_range[1], i, str(freq_range[1]), ha='left', va='center', color='black')

# Plot low frequency range species with a different color
for i, (species, freq_range) in enumerate(low_freq_species.items()):
    color = species_colors.get(species)
    plt.barh(i + len(high_freq_species), freq_range[1] - freq_range[0], left=freq_range[0], color=color, alpha=0.5, label='Low Frequency Range')
    plt.text(freq_range[0], i + len(high_freq_species), str(freq_range[0]), ha='right', va='center', color='black')
    plt.text(freq_range[1], i + len(high_freq_species), str(freq_range[1]), ha='left', va='center', color='black')

# Set y-axis ticks and labels
plt.yticks(range(len(high_freq_species) + len(low_freq_species)), list(high_freq_species.keys()) + list(low_freq_species.keys()))

# Add labels and title
plt.xlabel('Frequency (Hz)', weight='bold')
plt.ylabel('Bird Species', weight='bold')
plt.title('Frequency Ranges of Bird Species', weight='bold')

# Adjust x-axis limits
plt.xlim(-1000, 9000)

# Show plot
plt.grid(axis='x')
plt.tight_layout()


### Plotting accuracy

# Function to process folder data and calculate average confidence scores
def process_folder_data(folder_path):
    folder_data = {}
    
    for species_folder in os.listdir(folder_path):
        species_path = os.path.join(folder_path, species_folder)
        if not os.path.isdir(species_path):
            continue
        
        species_data = {'Scientific Name': species_folder.split('_')[0],
                        'Common Name': species_folder.split('_')[1],
                        'Confidence Scores': [],
                        'Other Species Counts': []}
        
        for file in os.listdir(species_path):
            if file.endswith('.csv'):
                file_path = os.path.join(species_path, file)
                df = pd.read_csv(file_path)
                
                # Extract confidence scores greater than 0.5 and not NaN
                confidence_scores = df[(df['Confidence'] > 0.5) & (~df['Confidence'].isna())]
                
                # Take the highest confidence score
                max_confidence = confidence_scores['Confidence'].max()
                
                if not np.isnan(max_confidence):  # Check if max_confidence is not NaN
                    species_data['Confidence Scores'].append(max_confidence)
                
                # Count other species with confidence scores > 0.5
                other_species_count = len(confidence_scores) - 1  # Subtract 1 for the current species
                species_data['Other Species Counts'].append(other_species_count)
        
        # Calculate average confidence score
        avg_confidence = np.mean(species_data['Confidence Scores'])
        species_data['Average Confidence'] = avg_confidence
        
        # Calculate average count of other species with confidence scores > 0.5
        avg_other_species_count = np.mean(species_data['Other Species Counts'])
        species_data['Average Other Species Count'] = avg_other_species_count
        
        folder_data[species_folder] = species_data
    
    return folder_data

# Process data for fairywrens and low frequency species
fairywren_data = process_folder_data("./example/fairywren")
low_freq_data = process_folder_data("./example/low-freq")

# Plot average highest confidence scores for fairywrens

plt.figure(figsize=(10, 6))
x_values = range(len(fairywren_data))  # Numeric values for x-axis
species_names = list(fairywren_data.keys())

for i, (species, data) in enumerate(fairywren_data.items()):
    plt.bar(i, data.get('Average Confidence', 0), label=data['Common Name'], color=species_colors[data['Common Name']])
    # Annotate each data point with the average confidence score
    plt.text(i, data.get('Average Confidence', 0), f"({data.get('Average Confidence', 0):.2f})", ha='right', va='center', color='black',
                bbox=dict(facecolor='white', edgecolor='none', pad=2))
plt.xticks(x_values, [data['Common Name'] for data in fairywren_data.values()])
plt.xlabel('Species', weight='bold')
plt.ylabel('Average Confidence', weight='bold')
plt.title('Average Confidence Scores for Fairywrens', weight='bold')
plt.tight_layout()


# Plot average highest confidence scores for low frequency species
plt.figure(figsize=(10, 6))
x_values = range(len(low_freq_data))  # Numeric values for x-axis
species_names = list(low_freq_data.keys())

for i, (species, data) in enumerate(low_freq_data.items()):
    plt.bar(i, data['Average Confidence'], label=data['Common Name'], color=species_colors[data['Common Name']])
    # Annotate each data point with the average confidence score
    plt.text(i, data['Average Confidence'], f"({data['Average Confidence']:.2f})", ha='right', va='center', color='black',
                bbox=dict(facecolor='white', edgecolor='none', pad=2))
plt.xticks(x_values, [data['Common Name'] for data in low_freq_data.values()])
plt.xlabel('Species', weight='bold')
plt.ylabel('Average Confidence', weight='bold')
plt.title('Average Confidence Scores for Low Frequency Species', weight='bold')
plt.tight_layout()



### Plotting Error

# Plot average counts of other species for fairywrens
plt.figure(figsize=(10, 6))
x_values = range(len(fairywren_data))  # Numeric values for x-axis
species_names = list(fairywren_data.keys())

for i, (species, data) in enumerate(fairywren_data.items()):
    plt.bar(i, data.get('Average Other Species Count', 0), label=data['Common Name'], color=species_colors[data['Common Name']])
    # Annotate each data point with the average count of other species
    plt.text(i, data.get('Average Other Species Count', 0), f"({data.get('Average Other Species Count', 0):.2f})", ha='right', va='center', color='black',
                bbox=dict(facecolor='white', edgecolor='none', pad=2))
plt.xticks(x_values, [data['Common Name'] for data in fairywren_data.values()])
plt.xlabel('Species', weight='bold')
plt.ylabel('Average Other Species Count', weight='bold')
plt.title('Average Counts of Other Species for Fairywrens', weight='bold')
plt.tight_layout()

# Low frequency species
plt.figure(figsize=(10, 6))
x_values = range(len(low_freq_data))  # Numeric values for x-axis
species_names = list(low_freq_data.keys())

for i, (species, data) in enumerate(low_freq_data.items()):
    plt.bar(i, data.get('Average Other Species Count', 0), label=data['Common Name'], color=species_colors[data['Common Name']])
    # Annotate each data point with the average count of other species
    plt.text(i, data.get('Average Other Species Count', 0), f"({data.get('Average Other Species Count', 0):.2f})", ha='right', va='center', color='black',
                bbox=dict(facecolor='white', edgecolor='none', pad=2))
plt.xticks(x_values, [data['Common Name'] for data in low_freq_data.values()])
plt.xlabel('Species', weight='bold')
plt.ylabel('Average Other Species Count', weight='bold')
plt.title('Average Counts of Other Species for Low Frequency Species', weight='bold')
plt.tight_layout()



plt.show()