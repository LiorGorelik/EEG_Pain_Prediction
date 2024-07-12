import os
import pandas as pd
from scipy.stats import spearmanr


def calculate_correlations(input_csv_path, output_folder_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_csv_path)

    # Get unique frequency bands
    unique_bands = df['Band'].unique()

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Iterate through unique frequency bands
    for band in unique_bands:
        band_df = df[df['Band'] == band]

        # Create a dictionary to store correlations for each channel pair
        correlations = {}

        # Get unique channels
        unique_channels = band_df['Electrode'].unique()

        # Iterate through unique channels
        for channel1 in unique_channels:
            vector1 = band_df[band_df['Electrode'] == channel1].set_index('Part')['Normalized_power']

            # Iterate through other unique channels
            for channel2 in unique_channels:
                if channel1 != channel2:
                    vector2 = band_df[band_df['Electrode'] == channel2].set_index('Part')['Normalized_power']

                    # Calculate spearmanr correlation
                    correlation, _ = spearmanr(vector1, vector2)

                    # Store the correlation in the dictionary
                    key = (channel1, channel2)
                    correlations[key] = correlation

        # Convert the dictionary to a DataFrame
        correlations_df = pd.DataFrame(list(correlations.items()), columns=['Channel1_Channel2', 'Spearman Correlation'])

        # Split the 'Channel1_Channel2' column into separate 'Channel1' and 'Channel2' columns
        correlations_df[['Channel1', 'Channel2']] = pd.DataFrame(correlations_df['Channel1_Channel2'].tolist(),
                                                                 index=correlations_df.index)
        correlations_df = correlations_df[['Channel1', 'Channel2', 'Spearman Correlation']]

        # Save the correlations DataFrame to a CSV file
        output_file_path = os.path.join(output_folder_path, f"PT#{df['Patient'].iloc[0]}_{band}_correlations.csv")
        correlations_df.to_csv(output_file_path, index=False)


def process_all_files(input_folder_path, output_folder_path):
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder_path):
        if filename.endswith(".csv"):
            input_csv_path = os.path.join(input_folder_path, filename)
            calculate_correlations(input_csv_path, output_folder_path)


if __name__ == "__main__":
    input_folder_path = r'C:\Users\Autologonuser\Desktop\ProjectB\output\output_files'
    output_correlation_folder_path = r'C:\Users\Autologonuser\Desktop\ProjectB\output\correlations_spear'

    # Process all Excel files in the input folder
    process_all_files(input_folder_path, output_correlation_folder_path)
