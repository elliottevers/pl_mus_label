from typing import List
import pickle
import cache
import json
import os
import subprocess


# CHORD = 'chord'
# CHORD_LIVE = 'chord_live'
# CHORD_SCORE = 'chord_score'
# FILE_CHORD_SCORE = '/some/filepath'
# FILE_CHORD_LIVE = '/some/filepath'


# def _get_dir_cache():
#     return os.path.dirname(os.path.abspath(cache.__file__))
#
#
# FILE_CLIPS_EXPORT = os.path.join(_get_dir_cache(), 'json', 'live', 'from_live.json')
#
# CLIPS_EXPORT = os.path.join(_get_dir_cache(), 'pickle', 'live', 'from_live.pkl')
#
# CLIPS_EXPORT_MID = os.path.join(_get_dir_cache(), 'midi', 'clips_export.mid')
#
# cache_map = {
#
# }


dir_projects = os.path.dirname('/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/tk_music_projects/')
file_log = os.path.join(dir_projects, '.log.txt')


def _get_name_project_most_recent():
    return subprocess.run(
        ['head', '-1', file_log],
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


def get_tuple_beats(filepath):
    obj_beat = from_pickle(filepath)
    return obj_beat['beat_start'], obj_beat['beat_end'], obj_beat['length_beats'], obj_beat['beatmap']


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


def create_dir_beat():
    return subprocess.run(
        ['mkdir', os.path.join(get_project_dir(), 'beat')],
        stdout=subprocess.PIPE
    )
