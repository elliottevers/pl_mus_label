from typing import List
from live import note as note_live
import json
from utils import utils
from postprocess import music_xml as postp_mxl


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

            # self.score[part]['notes'].append(
            #     ' '.join(
            #         [
            #             'notes',
            #             str(
            #                 (
            #                         len(json_read[part]['notes']) - 2
            #                 )
            #             )
            #         ]
            #     )
            # )

            # mode = 'polyphonic' if part == 'chord' else 'monophonic'

            # list_structs = postp_mxl.live_to_xml(
            #     note_live.NoteLive.parse_list(
            #         json_read[part]['notes']
            #     ),
            #     mode='monophonic'
            # )

            # note_live.NoteLive.parse_list(
            #     json_read[part]['notes']
            # )

    def get_part(self, name_part: str):  #  -> List[note_live.NoteLive]:
        return note_live.NoteLive.parse_list(
            self.score[name_part]['notes']
        )
