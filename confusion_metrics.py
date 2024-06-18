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

def calculate_metrics(confusion_matrix, species):
    metrics = []
    for i, spec in enumerate(species):
        tp = confusion_matrix[i, i]
        fp = np.sum(confusion_matrix[:, i]) - tp
        fn = np.sum(confusion_matrix[i, :]) - tp
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics.append({
            'Species': spec,
            'Precision': precision,
            'Recall': recall,
            'F1-score': f1_score
        })
    
    return metrics

def write_metrics_to_csv(metrics, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Species', 'Precision', 'Recall', 'F1-score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for metric in metrics:
            writer.writerow(metric)

def main():
    merged_file = 'merged.csv'
    output_dir = 'confusion_matrices/'
    output_file = 'confusion_matrix.csv'

    # Step 1: Read data from merged.csv
    data = read_merged_data(merged_file)

    # Step 2: Create confusion matrix
    confusion_matrix, species = create_confusion_matrix(data)

    # Step 3: Calculate metrics
    metrics = calculate_metrics(confusion_matrix, species)

    # Print metrics
    print("Metrics:")
    for metric in metrics:
        print(f"{metric['Species']}: Precision={metric['Precision']:.2f}, Recall={metric['Recall']:.2f}, F1-score={metric['F1-score']:.2f}")

    # Step 4: Write metrics to CSV file
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_path = os.path.join(output_dir, output_file)
    write_metrics_to_csv(metrics, output_file_path)
    print(f"Metrics saved in '{output_file_path}'")

if __name__ == '__main__':
    main()
