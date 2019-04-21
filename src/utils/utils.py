from typing import List
import pickle
import json
import os
import subprocess
from itertools import zip_longest
import numpy as np
import math
import librosa

dir_projects = os.path.dirname('/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/tk_music_projects/')

file_log = os.path.join(dir_projects, '.log.txt')


def parse_arg(arg):
    return arg if arg is None else arg.replace("\"", '')


def get_duration_s_audio(filename, use_warped=True) -> float:
    y, sr = librosa.load(
        filename
    )

    return float(
        librosa.get_duration(
            y=y,
            sr=sr
        )
    )


def get_beat_nearest(beatmap, s_beat):
    return min([abs(s_beat_beatmap - s_beat) for s_beat_beatmap in beatmap])


def get_num_beats(beatmap, s_beat_start, s_beat_end):
    return len(list(filter(lambda x: get_beat_nearest(beatmap, s_beat_start) <= x <= get_beat_nearest(beatmap, s_beat_end), beatmap)))


def b_use_warped():
    return os.path.exists(
        os.path.join(
            get_dirname_audio_warped(),

        )
    )


def rotate_items(dictionary, offset=0):
    return dict(zip(rotate(list(dictionary.keys()), offset), list(dictionary.values())))


def rotate(l, n):
    return l[n:] + l[:n]


def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx - 1
    else:
        return idx


def grouper(n, iterable, padvalue=None):
    """grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"""
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)


def most_common(lst):
    return max(set(lst), key=lst.count)


def write_name_project(name_project):
    return subprocess.Popen(
        ' '.join(['echo', name_project, '>>', file_log]),
        shell=True,
        stdout=subprocess.PIPE
    )


def _get_name_project_most_recent():
    return subprocess.run(
        ['tail', '-1', file_log],
        stdout=subprocess.PIPE
    ).stdout.rstrip().decode("utf-8")


def get_project_dir():
    return os.path.join(dir_projects, 'projects', _get_name_project_most_recent())


def get_dirname_audio():
    return os.path.join(get_project_dir(), 'audio')


def get_dirname_audio_warped():
    return os.path.join(get_project_dir(), 'audio_warped')


def get_dirname_tempo():
    return os.path.join(get_project_dir(), 'tempo')


def get_dirname_beat():
    return os.path.join(get_project_dir(), 'beat')


def get_dirname_score():
    return os.path.join(get_project_dir(), 'score')


def get_tuple_beats():
    obj_beat = from_pickle(
        os.path.join(
            get_dirname_beat(),
            _get_name_project_most_recent() + '.pkl'
        )
    )
    return (
        obj_beat['s_beat_start'],
        obj_beat['s_beat_end'],
        obj_beat['tempo'],
        obj_beat['beat_start'],
        obj_beat['beat_end'],
        obj_beat['length_beats'],
        obj_beat['beatmap']
    )


def intersection(former: List, latter: List) -> List:
    return [value for value in former if value in latter]


def to_pickle(object, filename):
    with open(filename, "wb") as f:
        pickle.dump(obj=object, file=f)


def from_pickle(filename):
    with open(filename, "rb") as input_file:
        return pickle.load(input_file)


def to_json_live(dict, filename_chords_to_live):
    with open(filename_chords_to_live, 'w') as outfile:
        json.dump(
            dict,
            outfile
        )


def create_dir_project():
    if os.path.exists(
        os.path.join(get_project_dir())
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', os.path.join(get_project_dir())],
            stdout=subprocess.PIPE
        )


def get_path_dir_audio():
    return os.path.join(get_project_dir(), 'audio')


def get_path_dir_video():
    return os.path.join(get_project_dir(), 'video')


def get_path_dir_audio_warped():
    return os.path.join(get_project_dir(), 'audio_warped')


def get_path_dir_video_warped():
    return os.path.join(get_project_dir(), 'video_warped')


def get_path_dir_session():
    return os.path.join(get_project_dir(), 'session')


def create_dir_audio():
    path_dir_audio = get_path_dir_audio()
    if os.path.exists(
            path_dir_audio
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', path_dir_audio],
            stdout=subprocess.PIPE
        )


def create_dir_video():
    path_dir_video = get_path_dir_video()
    if os.path.exists(
            path_dir_video
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', path_dir_video],
            stdout=subprocess.PIPE
        )


def create_dir_audio_warped():
    path_dir_audio_warped = get_path_dir_audio_warped()
    if os.path.exists(
            path_dir_audio_warped
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', path_dir_audio_warped],
            stdout=subprocess.PIPE
        )


def create_dir_video_warped():
    path_dir_video_warped = get_path_dir_video_warped()
    if os.path.exists(
            path_dir_video_warped
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', path_dir_video_warped],
            stdout=subprocess.PIPE
        )


def create_dir_session():
    path_dir_session = get_path_dir_session()
    if os.path.exists(
            path_dir_session
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', path_dir_session],
            stdout=subprocess.PIPE
        )


def create_dir_beat():
    if os.path.exists(
        os.path.join(get_project_dir(), 'beat')
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', os.path.join(get_project_dir(), 'beat')],
            stdout=subprocess.PIPE
        )


def create_dir_score():
    if os.path.exists(
        os.path.join(get_project_dir(), 'score')
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', os.path.join(get_project_dir(), 'score')],
            stdout=subprocess.PIPE
        )


def create_dir_part(name_part):
    if os.path.exists(
        os.path.join(get_project_dir(), 'score', name_part)
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', os.path.join(get_project_dir(), 'score', name_part)],
            stdout=subprocess.PIPE
        )


def create_dir_segment():
    if os.path.exists(
        os.path.join(get_project_dir(), 'score', 'segment')
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', os.path.join(get_project_dir(), 'score', 'segment')],
            stdout=subprocess.PIPE
        )


def create_dir_chord():
    if os.path.exists(
        os.path.join(get_project_dir(), 'score', 'chord')
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', os.path.join(get_project_dir(), 'score', 'chord')],
            stdout=subprocess.PIPE
        )


def create_dir_key_center():
    if os.path.exists(
        os.path.join(get_project_dir(), 'score', 'key_center')
    ):
        return
    else:
        return subprocess.run(
            ['mkdir', os.path.join(get_project_dir(), 'score', 'key_center')],
            stdout=subprocess.PIPE
        )


def get_file_json_comm():

    return os.path.join(
        dir_projects, 'json_live.json'
    )
