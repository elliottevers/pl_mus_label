import os
import pandas as pd
import numpy as np

dirname_repo = '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/music/'

dirname_read = '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/music/src/information_retrieval/out/hz_raw/'

filename_read = 'tswift_teardrops.csv'

filename_out = ''.join([filename_read.split('.')[0], '.txt'])

csv_melody = 'src/information_retrieval/out/hz_raw/tswift_teardrops.csv'

csv_melody = os.path.join(
    dirname_repo, csv_melody
)

melody_df = pd.read_csv(
    csv_melody,
    header=None,
    names=['ms', 'sample']
)

melody_df[melody_df['sample'] < 0] = 0

melody_df[melody_df.columns[-1]] = melody_df[melody_df.columns[-1]].astype(str).map(lambda entry: entry + ';')

melody_df.index = melody_df.index + 1

melody_df.to_csv(
    os.path.join(
        dirname_repo,
        os.path.join('src/postprocess/out/hz/', filename_out)
    ),
    header=False,
    index=True,
    columns=['sample']
)
