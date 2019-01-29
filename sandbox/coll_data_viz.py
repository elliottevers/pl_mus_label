import numpy as np

dirname = '/Users/elliottevers/Documents/git-repos.nosync/music'

filepath_write = dirname + '/' + 'sandbox/coll_data_viz.txt'

content = np.linspace(-1, 1, 512).tolist()

# with open(filepath_read, 'r') as f:
#     for line in f:
#         integer = round(float(line.rstrip().split(',')[1]))
#         if integer <= 0:
#             integer = 0
#         content.append(str(integer))

with open(filepath_write, 'w') as f:
    for i_line, line in enumerate(content):
        f.write(str(i_line + 1) + ',' + ' ' + str(line) + ';' + '\n')
