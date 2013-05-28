import csv

# Function for writing a list of probes
# holding spike data to CSV
# Format:
# name, data type, sampling period, data
# Note: data is output as an array of arrays

def write_data_to_csv(probe_list, filename='data'):

    # no probes, return
    if len(probe_list) == 0 or probe_list == None: return

    # create file for writing data
    if not filename.endswith('.csv'): filename += '.csv'
    csv_file=file(filename, 'wb')
    csv_writer = csv.writer(csv_file)
    # write headers
    csv_writer.writerow(['name', 'data type', 'sampling period', 'data'])

    for probe in probe_list:
        if probe.target_name.endswith('decoded'):
            data_type='decoded';
        elif probe.target_name.endswith('spikes'):
            data_type='spikes'
        else:
            print 'Do not know how to write %s to csv file' %probe.target_name
            assert False

        csv_writer.writerow([probe.target_name, data_type, probe.dt_sample, probe.get_data()])

    csv_file.close()
