import numpy as np

def bit_error_ratio():
    bit_stream = np.random.randint(0, 2, 10000)

    noise = np.random.choice([0, 1], size=10000, p=[0.99, 0.01])
    received_stream = np.bitwise_xor(bit_stream, noise)

    error_bits = np.sum(bit_stream != received_stream)
    total_bits = len(bit_stream)

    ber = error_bits / total_bits

    return ber

print(bit_error_ratio())

def abnormal_data_ratio():
    data = np.random.normal(loc=50, scale=5, size=1000)

    mean = np.mean(data)
    std_dev = np.std(data)
    threshold_low = mean - 3 * std_dev
    threshold_high = mean + 3 * std_dev

    abnormal_points = np.logical_or(data<threshold_low, data > threshold_high)
    num_abnormal = np.sum(abnormal_points)

    total_points = len(data)
    adr = num_abnormal / total_points

    return adr

print(abnormal_data_ratio())

# import psutil

# # Get CPU utilization percentage
# cpu_utilization = psutil.cpu_percent(interval=1)  # Measure over 1 second
# print(f"Processor Utilization: {cpu_utilization}%")
