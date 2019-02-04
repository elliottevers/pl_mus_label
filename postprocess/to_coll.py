import os

dirname_read = '/Users/elliottevers/Documents/Documents - Elliott’s MacBook Pro/git-repos.nosync/music/information_retrieval/output'

filename_read = 'melody_tswift_teardrops.csv'

filename_out = ''.join([filename_read.split('.')[0], '.txt'])

content = []

with open(os.path.join(dirname_read, filename_read), 'r') as f:
    for line in f:
        sample_hz = float(line.rstrip().split(',')[1])
        if sample_hz <= 0:
            sample_hz = 0
        content.append(str(sample_hz))

with open(os.path.join(dirname_read, filename_out), 'w') as f:
    for i_line, line in enumerate(content):
        f.write(str(i_line + 1) + ',' + ' ' + line + ';' + '\n')

print(os.path.join(dirname_read, filename_out))
