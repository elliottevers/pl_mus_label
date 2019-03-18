# from typing import List, Dict, Any, Optional, Tuple
# from live import note as note_live
# import json
# from message import messenger as lib_mes
# import music21
# import pandas as pd
# import numpy as np
# import argparse
# from postprocess import music_xml as postp_mxl
# from music import song
# from utils import utils
#
#
# def main(args):
#
#     filepath_frozen = '/Users/elliottevers/Downloads/score_frozen.json'
#
#     filename_out_max = str(args.filepath)
#
#     filename_to_max = '/Users/elliottevers/Downloads/to_live.json'
#
#     song_end_beats = 392
#
#     song_start_beats = 0
#
#     messenger = lib_mes.Messenger()
#
#     messenger.message(['running'])
#
#     # with open(filename_out_max) as f:
#     #     json_read = json.load(f)
#
#     # dict_write = dict(
#     #
#     # )
#
#     parts = ['melody', 'chord', 'bass', 'segment', 'key_center']
#
#     # TODO: for each part
#     def beat_to_gran(beat):
#         return (beat * 48) / 4  # assuming 16T quantization
#
#     def struct_to_df(struct, part, df_gran_master):
#
#         granularity = 1/48
#
#         epsilon = granularity/4  # for good measure
#
#         # TODO: rounding error on dataframe index was causing joins to go awry
#
#         # index = get_index_gran(
#         #     struct.offset,
#         #     struct.offset + struct.duration.quarterLength
#         # )
#
#         index_sliced_right_bound = df_gran_master.index[
#             df_gran_master.index <= struct.offset + struct.duration.quarterLength + epsilon
#         ]
#
#         index = index_sliced_right_bound[
#             index_sliced_right_bound >= struct.offset - epsilon
#         ]
#
#         if part == 'chord':
#             data = []
#             for _ in np.nditer(index):
#                 data.append(
#                     song.MeshSong.get_struct(struct)
#                 )
#             df = pd.DataFrame(
#                 data={part: data},
#                 index=index
#             )
#         else:
#             df = pd.DataFrame(
#                 data=np.full((len(index), 1), song.MeshSong.get_struct(struct)),
#                 index=index,
#                 columns=[part]
#             )
#
#         df.index.name = 'beat'
#
#         return df
#
#     def get_index_gran(start, end):
#         return np.linspace(
#             start=start,
#             stop=end,
#             num=beat_to_gran(end - start) + 1
#         )
#
#     index = get_index_gran(song_start_beats, song_end_beats)
#
#     df_gran_master = pd.DataFrame(
#         data=np.full(
#             (len(index), 1),
#             0  # TODO: does this make sense for all data
#         ),
#         index=index,
#         columns=['placeholder']
#     )
#
#     df_gran_master.index.name = 'beat'
#
#     # for part in utils.intersection(parts, list(json_read.keys())):
#     #
#     #     dict_write[part] = {
#     #
#     #     }
#     #
#     #     dict_write[part]['notes'] = [
#     #
#     #     ]
#     #
#     #     dict_write[part]['notes'].append(
#     #         ' '.join(
#     #             [
#     #                 'notes',
#     #                 str(
#     #                     (
#     #                         len(json_read[part]['notes']) - 2
#     #                     )
#     #                 )
#     #             ]
#     #         )
#     #     )
#     #
#     #     index = get_index_gran(
#     #         song_start_beats,
#     #         song_end_beats
#     #     )
#     #
#     #     df_gran = pd.DataFrame(
#     #         data=np.full(
#     #             (len(index), 1),
#     #             0  # TODO: does this make sense for all data
#     #         ),
#     #         index=index,
#     #         columns=[part]
#     #     )
#     #
#     #     df_gran.index.name = 'beat'
#     #
#     #     mode = 'polyphonic' if part == 'chord' else 'monophonic'
#     #
#     #     list_structs = postp_mxl.live_to_xml(
#     #         note_live.NoteLive.parse_list(
#     #             json_read[part]['notes']
#     #         ),
#     #         mode=mode
#     #     )
#         for struct_score in list_structs:
#
#             # dict_write[part]['notes'].append(
#             #     note.encode()
#             # )
#
#             df_gran.update(
#                 struct_to_df(
#                     struct_score,
#                     part=part,
#                     df_gran_master=df_gran_master
#                 )
#             )
#
#         # dict_write[part]['notes'].append(
#         #     ' '.join(['notes', 'done'])
#         # )
#
#         df_gran_master = pd.merge(
#             df_gran_master,
#             df_gran,
#             left_index=True,
#             right_index=True
#         )
#
#         # df_gran_master[part] = df_gran[part]
#         #
#         # df_gran_master.merge(
#         #     df_gran,
#         #     left_index=True,
#         #     right_index=True
#         # )
#
#     df_gran_master.drop(
#         ['placeholder'],
#         axis=1,
#         inplace=True
#     )
#
#     df_gran_master['chord'] = df_gran_master['chord'].apply(lambda val: None if val == 0 else val)
#
#     score = postp_mxl.df_grans_to_score(
#         df_gran_master,
#         parts=['melody', 'chord', 'bass']
#     )
#
#     # save mxl representation of score before loading to live
#
#     score_frozen = music21.freezeThaw.StreamFreezer(score)
#
#     score_frozen.write(fmt='pickle', fp=filepath_frozen)
#
#     thawer = music21.freezeThaw.StreamThawer()
#
#     thawer.open(fp=filepath_frozen)
#
#     # write to json file loaded by Ableton Live
#
#     with open(filename_to_max, 'w') as outfile:
#         json.dump(
#             dict_write,
#             outfile
#         )
#
#     #     dict_write[part] = {
#     #
#     #     }
#     #
#     #     dict_write[part]['notes'] = [
#     #
#     #     ]
#     #
#     #     dict_write[part]['notes'].append(
#     #         ' '.join(
#     #             [
#     #                 'notes',
#     #                 str(
#     #                     (
#     #                         len(json_read[part]['notes']) - 2
#     #                     )
#     #                 )
#     #             ]
#     #         )
#     #     )
#     #
#     #     for note in note_live.NoteLive.parse_list(json_read[part]['notes']):
#     #
#     #         note.beats_duration = note.beats_duration * 2
#     #
#     #         dict_write[part]['notes'].append(
#     #             note.encode()
#     #         )
#     #
#     #     dict_write[part]['notes'].append(
#     #         ' '.join(['notes', 'done'])
#     #     )
#     #
#     # with open(filename_to_max, 'w') as outfile:
#     #     json.dump(
#     #         dict_write,
#     #         outfile
#     #     )
#
#     messenger.message(['done'])
#
#     # messenger.message(['filepath', filename_to_max])
#
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='freeze Ableton Live clip as score')
#
#     parser.add_argument('filepath', help='filepath to json representation of midi on track')
#
#     args = parser.parse_args()
#
#     main(args)
