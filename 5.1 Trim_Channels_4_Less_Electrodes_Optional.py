import os
import pandas as pd

def filter_rows(file_path, values_to_keep, column_a, column_b):
    # Read the data from the Excel file
    data = pd.read_excel(file_path)

    # Define the condition to keep rows where both columns have values in the list
    condition = data.apply(lambda row: (row[column_a] in values_to_keep) and (row[column_b] in values_to_keep), axis=1)

    # Filter the data
    filtered_data = data[condition]

    # Save the filtered data back to the same file
    filtered_data.to_excel(file_path, index=False)
    print(f"Filtered file saved: {file_path}")

if __name__ == "__main__":
    # Define the folder path containing the Excel files
    folder_path = r'C:\Users\Autologonuser\Desktop\ProjectB\output'

    # Define the list of values to keep
    values_to_keep = [
        'FP1', 'Fz', 'F3', 'F7', 'FC5', 'FC1', 'C3', 'T7', 'CP5', 'CP1',
        'Pz', 'P3', 'P7', 'O1', 'Oz', 'O2', 'P4', 'P8', 'CP6', 'CP2',
        'Cz', 'C4', 'T8', 'FC6', 'FC2', 'F4', 'F8', 'Fp2', 'AF3', 'PO3',
        'PO4', 'AF4'
    ]

    # Get a list of all Excel files that start with "trimmed_merged_all_patients_correlations_" in the specified folder
    files = [file for file in os.listdir(folder_path) if
             file.startswith('trimmed_merged_all_patients_correlations_') and file.endswith('.xlsx')]

    # Define your actual column names here
    column_a = 'Channel1'  # First channel column
    column_b = 'Channel2'  # Second channel column

    # Iterate through each file and apply the filter
    for file in files:
        # Construct the full file path
        file_path = os.path.join(folder_path, file)

        # Filter the rows in the file
        filter_rows(file_path, values_to_keep, column_a, column_b)
