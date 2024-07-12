import os
import pandas as pd

def merge_correlations(master_file_path, correlations_folder_path, output_file_path, value):
    # Read the master correlations file
    master_df = pd.read_excel(master_file_path)

    # Get all files in the correlations folder that match the current value
    correlation_files = [f for f in os.listdir(correlations_folder_path) if f.endswith(".csv") and value in f]

    # Sort patient numbers in ascending order
    sorted_patient_numbers = sorted([int(f.split('_')[0].replace('PT#', '')) for f in correlation_files])

    # Iterate through correlation files and merge with the master DataFrame
    for patient_number in sorted_patient_numbers:
        patient_file = f"PT#{patient_number}_{value}_correlations.csv"
        file_path = os.path.join(correlations_folder_path, patient_file)

        # Read the correlation file
        correlation_df = pd.read_csv(file_path)

        # Merge with the master DataFrame based on 'Channel1' and 'Channel2'
        merged_column_name = str(patient_number)  # Convert to string for the column name
        master_df = pd.merge(master_df, correlation_df[['Channel1', 'Channel2', 'Spearman Correlation']],
                             on=['Channel1', 'Channel2'], how='left', suffixes=('', f'_{merged_column_name}'))

    # Save the merged DataFrame to the output file
    output_file_value_path = output_file_path.replace("delta", value)
    master_df.to_excel(output_file_value_path, index=False)

if __name__ == "__main__":
    master_file_path = r'C:\Users\Autologonuser\Desktop\ProjectB\output\all_possible correlations.xlsx'
    correlations_folder_path = r'C:\Users\Autologonuser\Desktop\ProjectB\output\correlations_spear'
    output_file_path_template = r'C:\Users\Autologonuser\Desktop\ProjectB\output\merged_all_patients_correlations_delta.xlsx'

    values = ['delta', 'theta', 'alpha1', 'alpha2', 'beta1', 'beta2', 'gamma']
    for value in values:
        output_file_path = output_file_path_template.replace("delta", value)
        merge_correlations(master_file_path, correlations_folder_path, output_file_path, value)
