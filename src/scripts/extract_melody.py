from message import messenger as mes
import argparse
from utils import utils
import os
from information_retrieval import extraction as ir
from preprocess import vamp as prep_vamp
from convert import hz as postp_hz

file_ts_coll = '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/tk_music_projects/ts_hz.txt'


def main(args):
    data_melody = ir.extract_melody(
        os.path.join(
            utils.get_dirname_audio_warped(),
            utils._get_name_project_most_recent() + '.wav'
        )
    )

    df_melody = prep_vamp.melody_to_df(
        (data_melody['vector'][0], data_melody['vector'][1]),
        index_type='s'
    )

    postp_hz.to_coll(
        df_melody,
        file_ts_coll
    )

    messenger = mes.Messenger()

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='extract melody from raw audio')

    parser.add_argument('--s', help='beat start')

    parser.add_argument('--e', help='beat end')

    args = parser.parse_args()

    main(args)

