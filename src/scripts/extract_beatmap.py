import sys
sys.path.insert(0, '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/music/src')
from information_retrieval import extraction as ir
from message import messenger as mes
import argparse
import numpy as np
import os
from utils import utils


def main(args):

    use_warped = args.m

    messenger = mes.Messenger()

    s_beat_start = float(utils.parse_arg(args.s_beat_start)) if utils.parse_arg(args.s_beat_start) else None

    s_beat_end = float(utils.parse_arg(args.s_beat_end)) if utils.parse_arg(args.s_beat_end) else None

    tempo = float(utils.parse_arg(args.tempo)) if utils.parse_arg(args.tempo) else None

    beat_start = float(utils.parse_arg(args.beat_start)) if utils.parse_arg(args.beat_start) else None

    beat_end = float(utils.parse_arg(args.beat_end)) if utils.parse_arg(args.beat_end) else None

    length_beats = float(utils.parse_arg(args.length_beats)) if utils.parse_arg(args.length_beats) else None

    filename_wav = os.path.join(
        utils.get_dirname_audio_warped() if use_warped else utils.get_dirname_audio(),
        utils._get_name_project_most_recent() + '.wav'
    )

    if args.a:
        s_beat_start = 0
        s_beat_end = utils.get_duration_s_audio(filename=filename_wav)


    # NB: to look up beat in beatmap, given a beat in Live
    # subtract one from measure, multply by 4, then subtract one beat
    # e.g., 74.1.1 => beatmap_manual[73*4 + 0]

    if use_warped:

        s_beat_start = 0

        s_beat_end = utils.get_duration_s_audio(
            filename=filename_wav
        )

        beatmap = np.linspace(
            0,
            s_beat_end,
            int(beat_end) - int(beat_start) + 1
        )

    else:

        beatmap = [val.to_float() for val in ir.extract_beats(filename_wav)]

        length_beats = utils.get_num_beats(beatmap, s_beat_start, s_beat_end)

        if args.double:
            beatmap = utils.double_beatmap(beatmap)
            length_beats = length_beats*2
        elif args.halve:
            beatmap = utils.halve_beatmap(beatmap)
            length_beats = length_beats/2

        # TODO: does this mean that all unwarped audio is assumed to be cropped?
        beat_start = 0

        beat_end = beat_start + length_beats - 1

    utils.create_dir_beat(

    )

    filepath_beatmap = os.path.join(
        utils.get_dirname_beat(),
        utils._get_name_project_most_recent() + '.pkl'
    )

    data_beats = {
        's_beat_start': s_beat_start,
        's_beat_end': s_beat_end,
        'tempo': tempo,
        'beat_start': float(beat_start),
        'beat_end': float(beat_end),
        'length_beats': float(length_beats),
        'beatmap': beatmap
    }

    if args.dump_estimates:
        for beat in beatmap:
            messenger.message(['beat', str(beat)])

    utils.to_pickle(
        data_beats,
        filepath_beatmap
    )

    messenger.message(['done', 'bang'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Estimate Beats')

    parser.add_argument('--s_beat_start', help='beat start marker in seconds')

    parser.add_argument('--s_beat_end', help='beat end marker in seconds')

    parser.add_argument('--tempo', help='tempo')

    parser.add_argument('--beat_start', help='start marker in beats')

    parser.add_argument('--beat_end', help='end marker in beats')

    parser.add_argument('--length_beats', help='length in beats')

    parser.add_argument('-m', help='manual', action='store_true')

    parser.add_argument('-a', help='automatically determine begin and end time', action='store_true')

    parser.add_argument('-dump_estimates', help='message the estimates', action='store_true')

    parser.add_argument('-double', help='double beats in estimate', action='store_true')

    parser.add_argument('-halve', help='halve beats in estimate', action='store_true')

    args = parser.parse_args()

    main(args)
