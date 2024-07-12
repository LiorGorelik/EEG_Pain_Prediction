import numpy as np
from scipy.signal import welch
from scipy.integrate import simps



def create_data(file_path):
    data_new = []
    with open(file_path, "r") as file:
        for line in file:
            values = line.strip().split()[1:]
            data_new.append(list(map(float, values)))

    data_area = []
    with open(file_path, "r") as file:
        for line in file:
            values = line.strip().split()[0:1]
            data_area.append(list(map(str, values)))

    inner_list_size = 2500
    jump_size = 1250
    all_segments = []

    #  every 5 seconds of data
    for i in range(0, len(data_new[0]), jump_size):
        start_index = min(i, len(data_new[0]) - inner_list_size)
        end_index = min(i + inner_list_size, len(data_new[0]))

        current_iteration_segments = []

        for inner_list in data_new:
            current_segment = inner_list[start_index:end_index]
            current_iteration_segments.append(current_segment)
        all_segments.append(current_iteration_segments)

    # Sample rate and desired cutoff frequencies
    fs = 512  # Replace with your actual sample rate
    lowcut = 0.5
    highcut = 40
    nyquist = 0.5 * fs
    low_c = lowcut / nyquist
    high_c = highcut / nyquist


    window = 'hamming'


    # Calculate PSD using Welch method
    # frequencies, psd = welch(data_eeg, fs=fs, nperseg=256)
    frequencies_all = []
    psd_all = []
    for i in range(len(all_segments)):
        frequencies, psd = welch(all_segments[i], fs=fs, nperseg=500)
        frequencies_all.append(frequencies)
        psd_all.append(psd)

    # Define the frequency bands of interest with corresponding colors
    frequency_bands = {
        'delta': (0.5, 4, 'yellow'),
        'theta': (4, 8, 'red'),
        'alpha1': (8, 10, 'blue'),
        'alpha2': (10, 13, 'lightblue'),
        'beta1': (13, 20, 'green'),
        'beta2': (20, 30, 'black'),
        'gamma': (30, 40, 'purple'),
    }

    # Calculate the area under each frequency band for each channel
    area_under_bands_list = []  # To store results for each iteration

    for j, psd in enumerate(psd_all):
        area_under_bands = {channel_index: [] for channel_index in range(len(psd))}

        for channel_index, channel_psd in enumerate(psd):
            channel_results = {}  # To store results for each channel

            for band_name, (low, high, color) in frequency_bands.items():
                band_indices = np.where((frequencies_all[j] >= low) & (frequencies_all[j] <= high))
                area = simps(channel_psd[band_indices], dx=frequencies_all[j][1] - frequencies_all[j][0])
                channel_results[band_name] = area

            area_under_bands[channel_index].append(channel_results)

        # Append the result for the current iteration to the list
        area_under_bands_list.append(area_under_bands)


    relative_sums_list = []  # To store results for each iteration
    for area_under_bands in area_under_bands_list:  # area_under_band is for each part in time
        relative_sums = [[] for _ in area_under_bands]  # Initialize a list for each part in time

        for k in range(len(area_under_bands)):
            total_area = np.sum(area_under_bands[k])
            total_sum = sum(total_area.values())
            for area, value in total_area.items():
                relative_sums[k].append(value / total_sum)

        # Append the result for the current iteration to the list
        relative_sums_list.append(relative_sums)  # each list contain the relative sums for each chanel for each part

    return all_segments, data_area, relative_sums_list
