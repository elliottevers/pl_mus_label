import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from intervaltree import IntervalTree, Interval
import music21
import math
import numpy as np


class MeshSong(object):

    tree_melody: IntervalTree

    tree_chord: IntervalTree

    tree_key_center: IntervalTree

    tree_bass: IntervalTree

    tree_segment: IntervalTree

    data_quantized: pd.DataFrame

    def __init__(self):
        self.data = None

    def quantize(
            self,
            beatmap,
            s_beat_start,
            s_beat_end,
            pos_first_beat,
            columns=[
                'melody',
                'bass',
                'chords',
                'segments'
            ]
    ) -> None:

        gran_map = MeshSong.get_gran_map(
            self.trim_beatmap(beatmap, s_beat_start, s_beat_end),
            pos_first_beat
        )

        self.data_quantized = self._get_maximum_overlap(gran_map, columns)

    def set_tree(self, interval_tree: IntervalTree, type: str) -> None:
        if type not in ['melody', 'chord', 'bass', 'segment', 'key_center']:
            raise('interval tree of type ' + type + ' not supported')
        # TODO: this is a bit scary now isn't it?
        setattr(self, 'tree_' + type, interval_tree)

    # TODO: put somewhere else
    @staticmethod
    def get_note(pitch_midi):
        if not pitch_midi or math.isinf(pitch_midi) or math.isnan(pitch_midi) or pitch_midi == 0:
            return None
        else:
            return music21.note.Note(pitch=music21.pitch.Pitch(midi=int(pitch_midi)))

    # TODO: remove, this is stupid
    @staticmethod
    def get_pitch_midi(pitch_midi):
        if not pitch_midi or math.isinf(pitch_midi) or math.isnan(pitch_midi) or pitch_midi == 0:
            return 0
        else:
            return pitch_midi

    @staticmethod
    def get_gran_map(beatmap, offset_first_beat, quantize='16T'):

        gran_map = dict()

        if quantize == '16T':
            num_samples = 49

        for beat, s in enumerate(beatmap[:-1], 1):
            index_beatmap = beat - 1
            beat_interpolated = np.linspace(beat + offset_first_beat, beat + 1 + offset_first_beat, num_samples)
            s_interpolated = np.linspace(beatmap[index_beatmap], beatmap[index_beatmap + 1], num_samples)
            gran_map.update(dict(zip(beat_interpolated, s_interpolated)))

        return gran_map

    # NB: s_beat_start and s_beat_end are determined by human
    @staticmethod
    def trim_beatmap(beatmap: List[float], s_beat_start, s_beat_end) -> List[float]:

        s_beat_first_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - s_beat_start))

        s_beat_last_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - s_beat_end))

        return list(filter(lambda beat: s_beat_first_quantized <= beat <= s_beat_last_quantized, beatmap))

    @staticmethod
    def get_overlap(top: Tuple, bottom: Tuple) -> float:
        if top[0] <= bottom[0] and top[1] >= bottom[0] and bottom[1] >= top[1]:
            return top[1] - bottom[0]
        elif bottom[0] <= top[0] and bottom[1] >= top[0] and top[1] >= bottom[1]:
            return bottom[1] - top[0]
        elif bottom[0] <= top[0] and bottom[1] >= top[1]:
            return top[1] - top[0]
        elif top[0] <= bottom[0] and top[1] >= bottom[1]:
            return bottom[1] - bottom[0]
        else:
            raise 'how did this happen'

    def _get_maximum_overlap(self, gran_map, columns):

        dfs_quantized: Dict[str, pd.DataFrame] = dict()

        col_to_tree_map = {}

        for name_col in columns:
            col_to_tree_map[name_col] = getattr(self, 'tree_' + name_col)

        for name_column in columns:

            column_s_quantized = []
            column_beat = []
            column = []

            beats = sorted(list(gran_map.keys()))
            endpoint_s_last = sorted(list(gran_map.values()))[0]

            # TODO: create an accumulator for automatic "diff"-ing

            for beat in beats:

                s = gran_map[beat]

                s_interval = (endpoint_s_last, s)

                tree = col_to_tree_map[name_column]

                overlapping_intervals = tree.overlap(
                    s_interval[0],
                    s_interval[1]
                )

                if len(list(overlapping_intervals)) < 1:
                    column.append(
                        None
                    )
                    column_beat.append(
                        beat
                    )
                    column_s_quantized.append(
                        s
                    )
                else:
                    interval_winner = max(
                        list(overlapping_intervals),
                        key=lambda interval: MeshSong.get_overlap(s_interval, interval)
                    )

                    column.append(
                        interval_winner.data
                    )
                    column_beat.append(
                        beat
                    )
                    column_s_quantized.append(
                        s
                    )

                endpoint_s_last = s

            dfs_quantized[name_column] = pd.DataFrame(
                data={
                    name_column: column,
                    'beat': column_beat,
                    's': column_s_quantized
                }
            ).set_index(
                ['beat', 's']
            )

        return dfs_quantized

    @staticmethod
    def get_struct(obj):
        if type(obj).__name__ == 'Chord':
            # return tuple(obj.intervalVector)
            return [str(p) for p in obj.pitches]
        elif type(obj).__name__ == 'Note':
            return obj.pitch.midi
        else:
            return obj

    @staticmethod
    def get_interval_tree(df: pd.DataFrame) -> IntervalTree:

        struct_last = df.iloc[0].values[0]
        index_struct_last = df.index[0]
        intervals_structs = []

        for row in df.iloc[1:, :].itertuples(index=True, name=True):
            index = row[0]
            struct_current = row[1]
            if struct_current != struct_last:
                intervals_structs.append(
                    Interval(
                        index_struct_last,
                        index,
                        MeshSong.get_struct(struct_current)
                    )
                )
                struct_last = struct_current
                index_struct_last = index

        return IntervalTree(
            Interval(begin, end, data)
            for begin, end, data in intervals_structs
         )
