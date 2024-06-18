import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def read_merged_data(merged_file):
    with open(merged_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    return data

def create_confusion_matrix(data):
    species = sorted(set(row['Species'] for row in data))
    true_species = sorted(set(row['True Species'] for row in data))
    num_species = len(species)
    
    confusion_matrix = np.zeros((num_species, num_species), dtype=int)
    
    species_dict = {species[i]: i for i in range(num_species)}
    
    for row in data:
        species_name = row['Species']
        true_species_name = row['True Species']
        tp_fp = row['TP.FP']
        
        if true_species_name and species_name:  # Check if species names are not empty
            if tp_fp == 'T':
                if true_species_name in species_dict and species_name in species_dict:
                    confusion_matrix[species_dict[true_species_name]][species_dict[species_name]] += 1
            elif tp_fp == 'F':
                if true_species_name in species_dict and species_name in species_dict:
                    confusion_matrix[species_dict[true_species_name]][species_dict[species_name]] += 1
    
    return confusion_matrix, species


def plot_confusion_matrix(confusion_matrix, species, output_dir):
    plt.figure(figsize=(10, 8))
    sns.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=species, yticklabels=species)
    plt.xlabel('Predicted Species')
    plt.ylabel('True Species')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'))
    plt.close()

def main():
    merged_file = 'merged.csv'
    output_dir = 'confusion_matrices/'

    # Step 1: Read data from merged.csv
    data = read_merged_data(merged_file)

    # Step 2: Create confusion matrix
    confusion_matrix, species = create_confusion_matrix(data)

    # Step 3: Plot and save confusion matrix
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plot_confusion_matrix(confusion_matrix, species, output_dir)
    print(f"Confusion matrix saved in '{output_dir}'")

if __name__ == '__main__':
    main()
