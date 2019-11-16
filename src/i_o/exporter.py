import json
from typing import List


class Exporter(object):
    def __init__(self):
        self.score = dict()

    def set_part(self, notes: List, name_part: str):
        self.score[name_part] = {

        }

        self.score[name_part]['notes'] = [

        ]

        self.score[name_part]['notes'].append(
            ' '.join(['notes', str(len(notes))])
        )

        for note in notes:
            self.score[name_part]['notes'].append(
                note.encode()
            )

        self.score[name_part]['notes'].append(
            ' '.join(['notes', 'done'])
        )

    def export(self, filepath):
        with open(filepath, 'w') as outfile:
            json.dump(
                self.score,
                outfile
            )
