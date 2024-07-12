import pandas as pd

def trim_and_save_excel(input_file_path, output_file_path):
    # Read the merged correlations file
    df = pd.read_excel(input_file_path)

    # Create a mask for rows where Column B comes before Column A alphabetically
    mask = df['Channel2'].astype(str) < df['Channel1'].astype(str)

    # Apply the mask to filter rows
    trimmed_df = df[~mask]

    # Save the trimmed DataFrame to a new Excel file
    trimmed_df.to_excel(output_file_path, index=False)

if __name__ == "__main__":
    base_input_file_path = r'C:\Users\Autologonuser\Desktop\ProjectB\output\merged_all_patients_correlations_{}.xlsx'
    base_output_file_path = r'C:\Users\Autologonuser\Desktop\ProjectB\output\trimmed_merged_all_patients_correlations_{}.xlsx'

    values = ['delta', 'theta', 'alpha1', 'alpha2', 'beta1', 'beta2', 'gamma']
    for value in values:
        input_file_path = base_input_file_path.format(value)
        output_file_path = base_output_file_path.format(value)
        trim_and_save_excel(input_file_path, output_file_path)