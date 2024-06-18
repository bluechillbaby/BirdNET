import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns

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
                        'Other Species Counts': {},  # Use a set to store unique other species names
                        }
        
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
                other_species = confidence_scores[confidence_scores['Common Name'] != species_data['Common Name']]['Common Name']
                for other_species_name in other_species:
                    species_data['Other Species Counts'][other_species_name] = species_data['Other Species Counts'].get(other_species_name, 0) + 1
        
        # Calculate average confidence score
        avg_confidence = np.mean(species_data['Confidence Scores'])
        species_data['Average Confidence'] = avg_confidence

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

### Plot Confusion Matrix
# Function to generate confusion matrix
def generate_confusion_matrix(data, species_names, zoom_out=False):
    y_true = []
    y_pred = []

    # Extract common names from species data
    data_species_names = [data[key]['Common Name'] for key in data]

    # Check if there are any missing labels or misformatted labels
    missing_labels = set(species_names) - set(data_species_names)
    if missing_labels:
        raise ValueError(f"The following labels are missing or misformatted in the data: {missing_labels}")

    # Iterate over species data
    for key, species_data in data.items():
        common_name = species_data['Common Name']
        avg_confidence = species_data['Average Confidence']

        # Add ground truth
        if isinstance(avg_confidence, np.ndarray):
            y_true.extend([common_name] * len(avg_confidence))
        else:
            y_true.append(common_name)

        # Add predicted classes based on average confidence
        if isinstance(avg_confidence, np.ndarray):
            y_pred.extend([common_name if conf > 0.1 else 'Other' for conf in avg_confidence])
        else:
            y_pred.append(common_name if avg_confidence > 0.1 else 'Other')

        # Add predicted classes based on other species counts
        for other_species_name, count in species_data['Other Species Counts'].items():
            if count > 0:
                y_pred.extend([other_species_name] * count)
                y_true.extend([common_name] * count)  # Assume the ground truth is the species itself

    # Generate confusion matrix
    confusion_mat = confusion_matrix(y_true, y_pred, labels=species_names)

    # Plot confusion matrix
    plt.figure(figsize=(12, 10))
    sns.heatmap(confusion_mat, annot=True, fmt='d', cmap='Blues', xticklabels=species_names, yticklabels=species_names)
    plt.xlabel('Predicted Label', weight='bold')
    plt.ylabel('True Label', weight='bold')
    plt.title('Confusion Matrix', weight='bold')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Zoom out if requested
    if zoom_out:
        plt.xlim(-0.5, len(species_names) - 0.5)
        plt.ylim(len(species_names) - 0.5, -0.5)

    plt.tight_layout()  # Adjust layout to prevent clipping of labels

generate_confusion_matrix(fairywren_data, [data['Common Name'] for data in fairywren_data.values()])
generate_confusion_matrix(low_freq_data, [data['Common Name'] for data in low_freq_data.values()])

plt.show()