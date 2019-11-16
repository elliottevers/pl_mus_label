from typing import List
from live import note as note_live
import json
from utils import utils


class Importer(object):
    def __init__(self, filepath_json_live):
        self.filepath_json_live = filepath_json_live
        self.score = dict()

    def load(self, parts: List[str]):

        with open(self.filepath_json_live) as f:
            json_read = json.load(f)

        for part in utils.intersection(parts, list(json_read.keys())):
            self.score[part] = {

            }

            self.score[part]['notes'] = json_read[part]['notes']

    def get_part(self, name_part: str) -> List[note_live.NoteLive]:
        return note_live.NoteLive.parse_list(
            self.score[name_part]['notes']
        )
