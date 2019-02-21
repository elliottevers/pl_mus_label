from typing import List
import pickle
import cache
import json


# CHORD = 'chord'
CHORD_LIVE = 'chord_live'
CHORD_SCORE = 'chord_score'
FILE_CHORD_SCORE = '/some/filepath'
FILE_CHORD_LIVE = '/some/filepath'


cache_map = {

}


def intersection(former: List, latter: List) -> List:
    return [value for value in former if value in latter]


def to_pickle(object, filename):
    with open(filename, "wb") as f:
        pickle.dump(obj=object, file=f)


def _get_dir_cache():
    return False


def get_path_cache(filename):
    raise 'not implemented'


def to_json_live(dict, filename_chords_to_live):
    with open(filename_chords_to_live, 'w') as outfile:
        json.dump(
            dict,
            outfile
        )
