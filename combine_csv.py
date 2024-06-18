import csv
import os

# Define output file name
output_file = "combined_data_sorted.csv"
validation_data_file = "BirdNet_validation.csv"

# Function to combine and sort data
def combine_and_sort_data(output_file, validation_file):
    # List to store combined data
    combined_data = []

    # Dictionary to store validation data for fast lookup
    validation_data = {}

    # Read validation data into dictionary
    with open(validation_file, 'r', newline='') as validation_csv:
        validation_reader = csv.DictReader(validation_csv)
        for row in validation_reader:
            validation_data[row['File']] = row

    # Traverse through current directory and subdirectories
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            folder_path = os.path.join(root, name)
            validate_folder_path = os.path.join(folder_path, f"{name}_Validate")

            # Function to process CSV files
            def process_csv_files(folder):
                csv_files = []
                # List CSV files in folder
                for file in os.listdir(folder):
                    if file.endswith(".csv"):
                        csv_files.append(os.path.join(folder, file))
                return csv_files

            # Process CSV files in parent folder
            parent_csv_files = process_csv_files(folder_path)
            for file in parent_csv_files:
                with open(file, 'r', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # Ensure we use the correct key based on the header row of BirdNet_validation.csv
                        file_name = row.get('File', None)
                        if file_name:
                            # Get corresponding validation data if exists
                            validation_row = validation_data.get(file_name, None)
                            if validation_row:
                                combined_data.append({
                                    'File': file_name,
                                    'Begin Time (s)': row.get('Begin Time (s)', ''),
                                    'End Time (s)': row.get('End Time (s)', ''),
                                    'Scientific Name': row.get('Scientific Name', ''),
                                    'Common Name': row.get('Common Name', ''),
                                    'Confidence': row.get('Confidence', ''),
                                    'TP.FP': validation_row['TP.FP'],
                                    'True.Species': validation_row['True.Species'],
                                    'Notes': validation_row['Notes']
                                })

            # Process CSV files in _Validate subfolder if exists
            if os.path.exists(validate_folder_path):
                validate_csv_files = process_csv_files(validate_folder_path)
                for file in validate_csv_files:
                    with open(file, 'r', newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            # Ensure we use the correct key based on the header row of BirdNet_validation.csv
                            file_name = row.get('File', None)
                            if file_name:
                                # Get corresponding validation data if exists
                                validation_row = validation_data.get(file_name, None)
                                if validation_row:
                                    combined_data.append({
                                        'File': file_name,
                                        'Begin Time (s)': row.get('Begin Time (s)', ''),
                                        'End Time (s)': row.get('End Time (s)', ''),
                                        'Scientific Name': row.get('Scientific Name', ''),
                                        'Common Name': row.get('Common Name', ''),
                                        'Confidence': row.get('Confidence', ''),
                                        'TP.FP': validation_row['TP.FP'],
                                        'True.Species': validation_row['True.Species'],
                                        'Notes': validation_row['Notes']
                                    })

    # Sort combined data by 'File'
    combined_data_sorted = sorted(combined_data, key=lambda x: x['File'])

    # Write combined and sorted data to output file
    with open(output_file, 'w', newline='') as combined_csv:
        writer = csv.DictWriter(combined_csv, fieldnames=['File', 'Begin Time (s)', 'End Time (s)', 'Scientific Name', 'Common Name', 'Confidence', 'TP.FP', 'True.Species', 'Notes'])
        writer.writeheader()
        for row in combined_data_sorted:
            writer.writerow(row)

    print(f"Combined and sorted data saved to {output_file}")

# Execute the function
if __name__ == "__main__":
    combine_and_sort_data(output_file, validation_data_file)
