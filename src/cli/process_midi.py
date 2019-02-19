from typing import List, Dict, Any, Optional, Tuple
from live import note as note_live
import json
from message import messenger as lib_mes

import argparse


def main(args):

    filename_out_max = str(args.filepath)

    filename_to_max = '/Users/elliottevers/Downloads/to_live.json'

    messenger = lib_mes.Messenger()

    messenger.message(['running'])

    with open(filename_out_max) as f:
        json_read = json.load(f)

    dict_write = dict(

    )

    def intersection(former: List[str], latter: List[str]) -> List[str]:
        return [value for value in former if value in latter]

    parts = ['melody', 'chord', 'bass', 'segment', 'key_center']

    for part in intersection(parts, list(json_read.keys())):

        dict_write[part] = {

        }

        dict_write[part]['notes'] = [

        ]

        dict_write[part]['notes'].append(
            ' '.join(
                [
                    'notes',
                    str(
                        (
                            len(json_read[part]['notes']) - 2
                        )
                    )
                ]
            )
        )

        for note in note_live.NoteLive.parse_list(json_read[part]['notes']):

            note.beats_duration = note.beats_duration * 2

            dict_write[part]['notes'].append(
                note.encode()
            )

        dict_write[part]['notes'].append(
            ' '.join(['notes', 'done'])
        )

    with open(filename_to_max, 'w') as outfile:
        json.dump(
            dict_write,
            outfile
        )

    messenger.message(['done'])

    messenger.message(['filepath', filename_to_max])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Midi I/O')

    parser.add_argument('filepath', help='filepath to json representation of midi on track')

    args = parser.parse_args()

    main(args)
