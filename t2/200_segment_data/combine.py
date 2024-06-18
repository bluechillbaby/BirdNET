import os
import csv
import re

def natural_sort_key(s):
    """
    Key function for natural sorting of filenames containing numbers.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def combine_csv_data(base_dir, output_file):
    combined_data = []

    # Collect filenames from BirdNet_validation.csv for exclusion
    excluded_files = set()
    validation_csv = "BirdNet_validation.csv"
    if os.path.exists(validation_csv):
        with open(validation_csv, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                excluded_files.add(row['File'])

    # Traverse through the base directory and process .csv files in folders and their subfolders
    for dir_name, _, files in os.walk(base_dir):
        for file_name in files:
            file_path = os.path.join(dir_name, file_name)
            if file_name.endswith('.csv') and dir_name != base_dir and file_name not in excluded_files:
                with open(file_path, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        combined_data.append({
                            'File Name': file_name,
                            'Begin Time (s)': row.get('Begin Time (s)', ''),
                            'End Time (s)': row.get('End Time (s)', ''),
                            'Scientific Name': row.get('Scientific Name', ''),
                            'Common Name': row.get('Common Name', ''),
                            'Confidence': row.get('Confidence', '')
                        })

    # Sort combined data by 'Common Name' and then by 'File Name' using natural sorting
    combined_data_sorted = sorted(combined_data, key=lambda x: (x['Common Name'], natural_sort_key(x['File Name'])))

    # Write combined and sorted data to output file
    with open(output_file, 'w', newline='') as combined_csv:
        writer = csv.DictWriter(combined_csv, fieldnames=['File Name', 'Begin Time (s)', 'End Time (s)', 'Scientific Name', 'Common Name', 'Confidence'])
        writer.writeheader()
        for row in combined_data_sorted:
            writer.writerow(row)

    print(f"Combined and sorted data saved to {output_file}")

if __name__ == "__main__":
    base_directory = "."  # Current directory, change if needed
    output_csv_file = "combined_data.csv"
    combine_csv_data(base_directory, output_csv_file)
