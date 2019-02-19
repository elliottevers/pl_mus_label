from typing import List, Dict, Any, Optional, Tuple
from live import note as note_live
import json
from message import messenger as lib_mes
import music21
import pandas as pd
import numpy as np
import argparse
from postprocess import music_xml as postp_mxl
from music import song


def main(args):

    filename_out_max = str(args.filepath)

    filename_to_max = '/Users/elliottevers/Downloads/to_live.json'

    song_end_beats = 392

    song_start_beats = 0

    messenger = lib_mes.Messenger()

    messenger.message(['running'])

    with open(filename_out_max) as f:
        json_read = json.load(f)

    dict_write = dict(

    )

    def intersection(former: List[str], latter: List[str]) -> List[str]:
        return [value for value in former if value in latter]

    parts = ['melody', 'chord', 'bass', 'segment', 'key_center']

    # TODO: for each part
    def beat_to_gran(beat):
        return (beat * 48) / 4  # assuming 16T quantization

    # def note_to_df(note, part):
    #     index = get_index_gran(note.beat_start, note.get_beat_end())
    #
    #     df = pd.DataFrame(
    #         data=np.full((len(index), 1), note.pitch),
    #         index=index,
    #         columns=[part]
    #     )
    #
    #     df.index.name = 'beat'
    #
    #     return df

    def struct_to_df(struct, part, df_gran_master):

        granularity = 1/48

        epsilon = granularity/4  # for good measure

        # TODO: rounding error on dataframe index was causing joins to go awry

        # index = get_index_gran(
        #     struct.offset,
        #     struct.offset + struct.duration.quarterLength
        # )

        index_sliced_right_bound = df_gran_master.index[
            df_gran_master.index <= struct.offset + struct.duration.quarterLength + epsilon
        ]

        index = index_sliced_right_bound[
            index_sliced_right_bound >= struct.offset - epsilon
        ]

        if part == 'chord':
            data = []
            for _ in np.nditer(index):
                data.append(
                    list(song.MeshSong.get_struct(struct))
                )
            df = pd.DataFrame(
                data={part: data},
                index=index
            )
        else:
            df = pd.DataFrame(
                data=np.full((len(index), 1), song.MeshSong.get_struct(struct)),
                index=index,
                columns=[part]
            )

        df.index.name = 'beat'

        return df

    def get_index_gran(start, end):
        return np.linspace(
            start=start,
            stop=end,
            num=beat_to_gran(end - start) + 1
        )

    # def parse_note_stream()

    index = get_index_gran(song_start_beats, song_end_beats)

    df_gran_master = pd.DataFrame(
        data=np.full(
            (len(index), 1),
            0  # TODO: does this make sense for all data
        ),
        index=index,
        columns=['placeholder']
    )

    df_gran_master.index.name = 'beat'

    for part in intersection(parts, list(json_read.keys())):
        # linearly spaced numpy array length of tracks in beats

        # actually, can convert straight to offset and duration

        # convert json to df_grans?

        # beat and quarter note duration are equivalent

        # for chords, gran -> Chord (chord interval tuple actually)

        # for chords, group into notes with the same offset and duration

        # for bass, melody, key center, segment, gran -> Note (pitch actually)

        # gran vectors, linearly spaced vectors -> gran dfs

        # gran dfs -> comparable objects

        # freeze stream

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

        index = get_index_gran(
            song_start_beats,
            song_end_beats
        )

        df_gran = pd.DataFrame(
            data=np.full(
                (len(index), 1),
                0  # TODO: does this make sense for all data
            ),
            index=index,
            columns=[part]
        )

        df_gran.index.name = 'beat'

        mode = 'polyphonic' if part == 'chord' else 'monophonic'

        # TODO: make a column named by the part
        # for note in note_live.NoteLive.parse_list(json_read[part]['notes']):
        list_structs = postp_mxl.live_to_xml(
            note_live.NoteLive.parse_list(
                json_read[part]['notes']
            ),
            mode=mode
        )
        for struct_score in list_structs:

            # dict_write[part]['notes'].append(
            #     note.encode()
            # )

            df_gran.update(
                struct_to_df(
                    struct_score,
                    part=part,
                    df_gran_master=df_gran_master
                )
            )

            testing = 1

            # df_gran.concat(
            #     struct_to_df(
            #         struct_score,
            #         part=part
            #     )
            # )

            # df_gran_master = pd.concat(
            #     [
            #         df_gran_master[~df_gran_master.index.isin(df_gran.index)],
            #         df_gran
            #     ]
            # )

        # dict_write[part]['notes'].append(
        #     ' '.join(['notes', 'done'])
        # )

        df_gran_master = pd.merge(
            df_gran_master,
            df_gran,
            left_index=True,
            right_index=True
        )

        # df_gran_master[part] = df_gran[part]
        #
        # df_gran_master.merge(
        #     df_gran,
        #     left_index=True,
        #     right_index=True
        # )

    df_gran_master.drop(
        ['placeholder'],
        axis=1,
        inplace=True
    )

    exit(0)

    with open(filename_to_max, 'w') as outfile:
        json.dump(
            dict_write,
            outfile
        )

        # note = note_live.NoteLive(
        #     pitch=60,
        #     beat_start=2,
        #     beats_duration=3,
        #     velocity=90,
        #     muted=0
        # )


        def df_to_df_comparable():
            return False




            # big = pd.DataFrame([1, 2, 3, 4], index=[.25, .5, .75, 1])
            # little = pd.DataFrame([9, 10], index=[.5, .75])
            # big.update(little)


        # pd.DataFrame(
        #     timeseries,
        #     index=grans
        # )
        #
        # return pd.merge(
        #     pd.merge(
        #         pd.merge(
        #             dfs_quantized['melody'],
        #             dfs_quantized['bass'],
        #             left_index=True,
        #             right_index=True
        #         ),
        #         dfs_quantized['chord'],
        #         left_index=True,
        #         right_index=True
        #     ),
        #     dfs_quantized['segment'],
        #     left_index=True,
        #     right_index=True
        # ).sort_index(
        # )
        #
        #
        # # TODO: for each part
        # def beat_to_gran(beat):
        #     return beat * 48  # assuming 16T quantization
        #
        # for i_part, name_part in enumerate(parts):
        #     return False
        #
        # def gran_vector_from_offset_and_duration(offset=0, duration=1):
        #     return [0, 0, 0, (1,2,2,2,2), 0, )]
        #
        #     def _get_maximum_overlap(self, gran_map, columns):
        #
        #         dfs_quantized: Dict[str, pd.DataFrame] = dict()
        #
        #         col_to_tree_map = {
        #             'melody': self.tree_melody,
        #             'bass': self.tree_bass,
        #             'chord': self.tree_chord,
        #             'segment': self.tree_segment
        #             # 'key_center': self.tree_key_center
        #         }
        #
        #         for name_column in columns:
        #
        #             column_s_quantized = []
        #             column_beat = []
        #             column = []
        #
        #             beats = sorted(list(gran_map.keys()))
        #             endpoint_s_last = sorted(list(gran_map.values()))[0]
        #
        #             for beat in beats[:-1]:
        #
        #                 s = gran_map[beat]
        #
        #                 s_interval = (endpoint_s_last, s)
        #
        #                 tree = col_to_tree_map[name_column]
        #
        #                 overlapping_intervals = tree.overlap(
        #                     s_interval[0],
        #                     s_interval[1]
        #                 )
        #
        #                 if len(list(overlapping_intervals)) < 1:
        #                     column.append(
        #                         None
        #                     )
        #                     column_beat.append(
        #                         beat
        #                     )
        #                     column_s_quantized.append(
        #                         s
        #                     )
        #                 else:
        #                     interval_winner = max(
        #                         list(overlapping_intervals),
        #                         key=lambda interval: MeshSong.get_overlap(s_interval, interval)
        #                     )
        #
        #                     column.append(
        #                         interval_winner.data
        #                     )
        #                     column_beat.append(
        #                         beat
        #                     )
        #                     column_s_quantized.append(
        #                         s
        #                     )
        #
        #                 endpoint_s_last = s
        #
        #             dfs_quantized[name_column] = pd.DataFrame(
        #                 data={
        #                     name_column: column,
        #                     'beat': column_beat,
        #                     's': column_s_quantized
        #                 }
        #             ).set_index(
        #                 ['beat', 's']
        #             )
        #
        #         # TODO: segments, after they are fixed
        #         return pd.merge(
        #             pd.merge(
        #                 pd.merge(
        #                     dfs_quantized['melody'],
        #                     dfs_quantized['bass'],
        #                     left_index=True,
        #                     right_index=True
        #                 ),
        #                 dfs_quantized['chord'],
        #                 left_index=True,
        #                 right_index=True
        #             ),
        #             dfs_quantized['segment'],
        #             left_index=True,
        #             right_index=True
        #         ).sort_index(
        #         )



        score = music21.stream.Score()

        for i_part, name_part in enumerate(parts):

            part = music21.stream.Part()

            part.id = name_part

            df_grans['event'] = (df_grans[name_part].shift(1) != df_grans[name_part]).astype(int).cumsum()

            df_events = df_grans.reset_index().groupby([name_part, 'event'])[column_index].apply(np.array)

            beat_to_struct_score = dict()

            for i, span in df_events.iteritems():
                struct = i[0]

                beat_start = span[0]

                beat_end = span[-1]

                struct_score = get_struct_score(struct, name_part=name_part)

                struct_score.duration = music21.duration.Duration(
                    beat_end - beat_start + 1 / 48
                )

                beat_to_struct_score[beat_start] = struct_score

            measure = music21.stream.Measure()

            for beat in df_grans.index.get_level_values(0).tolist():
                if int(beat) == beat and int(beat) % 4 == 0:
                    part.append(measure)
                    measure = music21.stream.Measure()

                if beat in beat_to_struct_score:
                    struct_score = beat_to_struct_score[beat]
                    measure.append(
                        struct_score
                    )

            score.insert(i_part, part)
    #     dict_write[part] = {
    #
    #     }
    #
    #     dict_write[part]['notes'] = [
    #
    #     ]
    #
    #     dict_write[part]['notes'].append(
    #         ' '.join(
    #             [
    #                 'notes',
    #                 str(
    #                     (
    #                         len(json_read[part]['notes']) - 2
    #                     )
    #                 )
    #             ]
    #         )
    #     )
    #
    #     for note in note_live.NoteLive.parse_list(json_read[part]['notes']):
    #
    #         note.beats_duration = note.beats_duration * 2
    #
    #         dict_write[part]['notes'].append(
    #             note.encode()
    #         )
    #
    #     dict_write[part]['notes'].append(
    #         ' '.join(['notes', 'done'])
    #     )
    #
    # with open(filename_to_max, 'w') as outfile:
    #     json.dump(
    #         dict_write,
    #         outfile
    #     )

    messenger.message(['done'])

    # messenger.message(['filepath', filename_to_max])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='freeze Ableton Live clip as score')

    parser.add_argument('filepath', help='filepath to json representation of midi on track')

    args = parser.parse_args()

    main(args)
