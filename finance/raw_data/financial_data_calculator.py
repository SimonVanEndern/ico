

def calculate_for_timestamp(timestamp, data_before, data_after):
    output = data_before["data"]
    difference_data = data_after["data"] - data_before["data"]
    difference_time = data_after["time"] - data_before["time"]
    slope = difference_data / difference_time
    output += slope * (timestamp - data_before["time"])
    return output


# End is excluded
def calculate_series_for_timestamp(start, end, step, data):
    current_data_index = 0
    output = []
    for timestamp in range(start, end, step):
        while not (data[current_data_index]["time"] <= timestamp <= data[current_data_index + 1]["time"]):
            current_data_index += 1

            if current_data_index + 1 >= len(data):
                return output

        calculated_data = calculate_for_timestamp(timestamp, data[current_data_index], data[current_data_index + 1])
        output.append((timestamp, calculated_data))

    return output
