import csv
from functions_new import *
import os

if __name__ == "__main__":
    base_path = r'C:\Users\Autologonuser\Desktop\ProjectB\data\pt#{}'
    output_directory = r'C:\Users\Autologonuser\Desktop\ProjectB\output'

    number = 0
    frequency_bands = {
        'delta': (0.5, 4, 'yellow'),
        'theta': (4, 8, 'red'),
        'alpha1': (8, 10, 'blue'),
        'alpha2': (10, 13, 'lightblue'),
        'beta1': (13, 20, 'green'),
        'beta2': (20, 30, 'black'),
        'gamma': (30, 40, 'purple'),
    }
    freq_lst = list(frequency_bands.keys())

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for number in range(0, 100):  # Change 101 to the desired range
        file_name = os.path.join(output_directory, f"output_file_{number}.csv")  # Adjust the file name as needed
        file_path = base_path.format(number) + ".dat"
        if os.path.exists(file_path):
            print(file_path)
            data_new, data_area, relative_sums_list = create_data(file_path)
            with open(file_name, "w", newline='') as fi:
                writer = csv.writer(fi)
                writer.writerow(['Patient', 'Electrode', 'Band', 'Normalized_power', 'Part'])

                for i, relative_sums_values in enumerate(relative_sums_list):
                    part = i + 1
                    N = len(data_area)
                    for j in range(N):
                        for idx, band in enumerate(frequency_bands):
                            writer.writerow(
                                [number, data_area[j][0], freq_lst[idx], relative_sums_values[j][idx], part])
