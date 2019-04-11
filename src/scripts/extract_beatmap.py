from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
import numpy as np
import librosa
import os
from utils import utils


def main(args):
    messenger = mes.Messenger()

    # from start marker
    beat_start_marker = args.s.replace("\"", '')

    # from end marker
    beat_end_marker = args.e.replace("\"", '')

    beat_loop_bracket_lower = args.l.replace("\"", '')

    beat_loop_bracket_upper = args.u.replace("\"", '')

    length_beats = args.length_beats.replace("\"", '')

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
        beatmap = np.linspace(
            0,
            float(duration_s_audio),
            int(beat_end_marker) - int(beat_start_marker) + 1 - 4
        )
    else:
        beatmap = ir.extract_beats(
            filename_wav
        )

    utils.create_dir_beat(

    )

    filepath_beatmap = os.path.join(
        utils.get_dirname_beat(),
        utils._get_name_project_most_recent() + '.pkl'
    )

    data_beats = {
        'beat_start_marker': int(beat_start_marker),
        'beat_end_marker': int(beat_end_marker),
        'beat_loop_bracket_lower': int(beat_loop_bracket_lower),
        'beat_loop_bracket_upper': int(beat_loop_bracket_upper),
        'length_beats': int(length_beats),
        'beatmap': beatmap
    }

    utils.to_pickle(
        data_beats,
        filepath_beatmap
    )

    messenger.message(['done'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Estimate Beats')

    parser.add_argument('--s', help='beat start marker')

    parser.add_argument('--e', help='beat end marker')

    parser.add_argument('--l', help='beat loop bracket lower')

    parser.add_argument('--u', help='beat loop bracket upper')

    parser.add_argument('--length-beats', help='length in beats')

    parser.add_argument('-m', help='manual', action='store_true')

    args = parser.parse_args()

    main(args)
