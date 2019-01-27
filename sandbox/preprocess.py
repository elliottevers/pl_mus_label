dirname = '/Users/elliottevers/Documents/git-repos.nosync/music'

filename_csv = 'sandbox/melody.csv'

filepath_read = dirname + '/' + filename_csv

filepath_write = dirname + '/' + 'sandbox/write.txt'

content = []

with open(filepath_read, 'r') as f:
    for line in f:
        integer = round(float(line.rstrip().split(',')[1]))
        if integer <= 0:
            integer = 0
        content.append(str(integer))

with open(filepath_write, 'w') as f:
    for i_line, line in enumerate(content):
        f.write(str(i_line + 1) + ',' + ' ' + line + ';' + '\n')
