from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
import numpy as np
import librosa
from information_retrieval import extraction
import os
from utils import utils


def main(args):
    messenger = mes.Messenger()

    # from start marker
    beat_start = args.s

    # from end marker
    beat_end = args.e

    # path wav warped
    filename_wav = os.path.join(
        utils.get_dirname_audio_warped(),
        utils._get_name_project_most_recent() + '.wav'
    )

    y, sr = librosa.load(
        filename_wav
    )

    duration_s_audio = librosa.get_duration(
        y=y,
        sr=sr
    )

    # NB: to look up beat in beatmap, subtract one from measure, multply by 4, then subtract one beat
    # e.g., 74.1.1 => beatmap_manual[73*4 + 0]

    if args.m:
        beatmap_manual = np.linspace(
            0,
            float(duration_s_audio),
            int(beat_end) - int(beat_start) + 1 - 4
        )
    else:
        return

    # beatmap_estimated = ir.extract_beats(
    #     filename_wav
    # )

    utils.create_dir_beat(

    )

    filepath_beatmap = os.path.join(
        utils.get_dirname_beat(),
        utils._get_name_project_most_recent() + '.pkl'
    )

    utils.to_pickle(
        beatmap_manual,
        filepath_beatmap
    )

    beatmap_thawed = utils.from_pickle(
        filepath_beatmap
    )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Estimate Beats')

    # parser.add_argument('filepath', help='audio file from which to extract beat estimates')

    parser.add_argument('--s', help='beat start')

    parser.add_argument('--e', help='beat end')

    parser.add_argument('-m', help='manual', action='store_true')

    args = parser.parse_args()

    main(args)
