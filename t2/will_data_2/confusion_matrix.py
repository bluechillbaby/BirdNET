import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import numpy as np

# Function to normalize species names
def normalize_species(species):
    species = species.strip().lower()
    if "corvid" in species:
        return "Corvid"
    elif "pipit" in species:
        return "Pipit"
    else:
        return species.capitalize()

# Load the data
file_path = 'BirdNet_validation.csv'  # Update with the correct path if needed
data = pd.read_csv(file_path)

# Filter out entries with "?" in True.Species
data = data[data['True.Species'] != '?']

# Fill NaN values in True.Species with an empty string
data['True.Species'] = data['True.Species'].fillna('')

# Define additional non-bird sounds
non_bird_sounds = {"Wind", "Insects", "Plane", "White noise", "Kangaroo jumping"}

# Normalize species names in both columns
data['Species'] = data['Species'].apply(normalize_species)
data['True.Species'] = data['True.Species'].apply(lambda x: '&'.join(normalize_species(s) for s in x.split('&')) if x else '')

# Get a list of unique species from both columns
all_species = set(data['Species']).union(set(data['True.Species'].str.split('&').sum()))

# Add non-bird sounds to the set of all species
all_species = all_species.union(non_bird_sounds)

# Strip any leading/trailing whitespace from species names
all_species = {species.strip() for species in all_species}

# Initialize lists to hold the true and predicted values for the combined confusion matrix
true_combined = []
pred_combined = []

# Populate the lists
for index, row in data.iterrows():
    predicted_species = row['Species']
    if row['True.Species']:
        true_species_list = str(row['True.Species']).split('&')
    else:
        true_species_list = [predicted_species] if row['TP.FP'] == 'T' else []

    for true_species in true_species_list:
        true_combined.append(true_species.strip())
        pred_combined.append(predicted_species.strip())

# Create a combined confusion matrix with all species
unique_labels_all = sorted(all_species)
cm_all = confusion_matrix(true_combined, pred_combined, labels=unique_labels_all)

# Get a list of unique species only from the 'Species' column
species_labels = sorted(set(data['Species']))

# Include a combined 'Non-bird' category for the filtered confusion matrix
def categorize_non_bird_sounds(species, non_bird_sounds):
    if species in non_bird_sounds:
        return 'Non-bird'
    return species

# Categorize non-bird sounds in the true_combined and pred_combined lists
true_combined_filtered = [categorize_non_bird_sounds(species, non_bird_sounds) for species in true_combined]
pred_combined_filtered = [categorize_non_bird_sounds(species, non_bird_sounds) for species in pred_combined]

# Add 'Non-bird' to the species_labels if any non-bird sounds are present
if any(species in non_bird_sounds for species in true_combined + pred_combined):
    species_labels.append('Non-bird')

# Create a combined confusion matrix with filtered species
cm_filtered = confusion_matrix(true_combined_filtered, pred_combined_filtered, labels=species_labels)

# Function to plot confusion matrix
def plot_confusion_matrix(cm, labels, title):
    plt.figure(figsize=(20, 15))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.ylabel('True Species')
    plt.xlabel('Predicted Species')
    plt.title(title)
    plt.show()

# Plot the combined confusion matrix with all species
plot_confusion_matrix(cm_all, unique_labels_all, 'Combined Confusion Matrix with All Species')

# Plot the combined confusion matrix with filtered species and non-bird category
plot_confusion_matrix(cm_filtered, species_labels, 'Combined Confusion Matrix with Filtered Species and Non-bird Sounds')
