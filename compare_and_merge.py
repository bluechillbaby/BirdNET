import csv

def merge_data(combined_data_file, validation_data_file, output_file):
    # Read combined data
    with open(combined_data_file, 'r', newline='', encoding='utf-8-sig') as combined_csv:
        combined_reader = csv.DictReader(combined_csv)
        combined_data = list(combined_reader)

    # Read validation data
    with open(validation_data_file, 'r', newline='', encoding='utf-8-sig') as validation_csv:
        validation_reader = csv.DictReader(validation_csv)
        validation_data = list(validation_reader)

    # Prepare output file
    fieldnames = ['File Name', 'Species', 'Validation Confidence', 'Combined Confidence', 'TP.FP', 'True Species']
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as output_csv:
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()

        # Merge data based on matching beginning of file names
        for combined_row in combined_data:
            for validation_row in validation_data:
                # Extracting the beginning part of the file names
                combined_file_name = combined_row['File Name'].split('.')[0]
                validation_file_name = validation_row['File Name'].rsplit('.', 1)[0]
                
                # Check if the beginning parts match
                if combined_file_name.startswith(validation_file_name) or validation_file_name.startswith(combined_file_name):
                    # Prepare data for writing
                    merged_row = {
                        'File Name': combined_row['File Name'],
                        'Species': combined_row['Common Name'],  # Assuming 'Common Name' is the species
                        'Validation Confidence': validation_row['Confidence'],
                        'Combined Confidence': combined_row['Confidence'],
                        'TP.FP': validation_row['TP.FP'],
                        'True Species': validation_row['True.Species']
                    }
                    # Write merged row to output file
                    writer.writerow(merged_row)
                    # Print for debugging
                    # print(f"Merged: {merged_row}")

# Example usage
combined_data_file = 'combined_data.csv'
validation_data_file = 'BirdNet_validation.csv'
output_file = 'merged.csv'

merge_data(combined_data_file, validation_data_file, output_file)
