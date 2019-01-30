import numpy as np
from scipy import signal

dirname = '/Users/elliottevers/Documents/git-repos.nosync/music'

filename_txt = 'sandbox/melody.csv'

filepath_read = dirname + '/' + filename_txt

filepath_write = dirname + '/' + 'sandbox/write_decimate.txt'

factor_downsample = 2

content = []

with open(filepath_read, 'r') as f:
    for line in f:
        integer = round(float(line.rstrip().split(',')[1]))
        # if integer <= 0:
        #     integer = 0
        content.append(str(integer))

filtered = np.round(signal.decimate(np.array(content, dtype=np.float), factor_downsample))

filtered[filtered <= 0] = 0

filtered_list = filtered.astype(dtype=np.int).tolist()

with open(filepath_write, 'w') as f:
    for i_line, line in enumerate(filtered_list):
        f.write(str(i_line + 1) + ',' + ' ' + str(line) + ';' + '\n')
