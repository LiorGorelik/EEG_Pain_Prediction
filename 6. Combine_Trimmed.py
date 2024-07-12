import pandas as pd

def combine_and_rename_columns(input_file_path, output_file_path):
    # Read the trimmed correlations file
    df = pd.read_excel(input_file_path)

    # Combine 'Channel1' and 'Channel2' into 'Combined Channel'
    df['Combined Channel'] = df['Channel1'].astype(str) + '_X_' + df['Channel2'].astype(str)

    # Drop the original 'Channel1' and 'Channel2' columns
    df = df.drop(columns=['Channel1', 'Channel2'])

    # Rename the remaining columns from 'Spearman Correlation_#' to just '#'
    new_column_names = []
    for col in df.columns[:-1]:  # Exclude the last column which is 'Combined Channel'
        if col == 'Spearman Correlation':
            new_column_names.append('1')
        elif col.startswith('Spearman Correlation_'):
            new_column_names.append(col.split('_')[-1])
        else:
            new_column_names.append(col)

    # Add 'Combined Channel' as the first column
    new_column_names = ['Combined Channel'] + new_column_names

    # Reorder the DataFrame columns
    df = df[['Combined Channel'] + [col for col in df.columns if col != 'Combined Channel']]

    # Assign the new column names to the DataFrame
    df.columns = new_column_names

    # Save the modified DataFrame to a new Excel file
    df.to_excel(output_file_path, index=False)

if __name__ == "__main__":
    base_input_file_path = r'C:\Users\Autologonuser\Desktop\ProjectB\output\trimmed_merged_all_patients_correlations_{}.xlsx'
    base_output_file_path = r'C:\Users\Autologonuser\Desktop\ProjectB\output\Combined_After_Trim_32_{}.xlsx'

    values = ['delta', 'theta', 'alpha1', 'alpha2', 'beta1', 'beta2', 'gamma']
    for value in values:
        input_file_path = base_input_file_path.format(value)
        output_file_path = base_output_file_path.format(value)
        combine_and_rename_columns(input_file_path, output_file_path)
