import pandas as pd
from typing import List, Dict, Tuple
from intervaltree import IntervalTree, Interval
import numpy as np
from utils import utils


class MeshScore(object):

    tree_melody: IntervalTree

    tree_chord: IntervalTree

    tree_key_center: IntervalTree

    tree_bass: IntervalTree

    tree_segment: IntervalTree

    tree_beatmap: IntervalTree

    data_quantized: pd.DataFrame

    def __init__(self):
        self.data = None

    def set_tree(self, interval_tree: IntervalTree, type: str) -> None:
        if type not in ['melody', 'chord', 'bass', 'segment', 'key_center', 'beatmap']:
            raise('interval tree of type ' + type + ' not supported')
        # TODO: please make less dynamic
        setattr(self, 'tree_' + type, interval_tree)

    def quantize(
            self,
            beatmap,
            s_beat_start,
            s_beat_end,
            columns
    ) -> None:
        # TODO: if we trim the beatmap to only consider beats between the start and end beat, why do we need the position of the first beat?
        # TODO: this may have only been only incidentally working because the "beat_start_marker" has always been 0
        gran_map = MeshScore.get_gran_map(
            self.trim_beatmap(beatmap, s_beat_start, s_beat_end)
        )

        self.data_quantized = self._get_maximum_overlap(gran_map, columns)

    # NB: this, along with quantizing, monophonifies things
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
            beat_last = beats[0]

            # for beat in beats:
            for beat in beats[1:]:

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
                        beat_last
                    )
                    column_s_quantized.append(
                        endpoint_s_last
                    )
                else:
                    interval_winner = max(
                        list(overlapping_intervals),
                        key=lambda interval: MeshScore.get_overlap(s_interval, interval)
                    )

                    column.append(
                        interval_winner.data
                    )
                    column_beat.append(
                        beat_last
                    )
                    column_s_quantized.append(
                        endpoint_s_last
                    )

                endpoint_s_last = s
                beat_last = beat

            # outside of loop now
            if len(list(overlapping_intervals)) < 1:
                column.append(
                    None
                )
                column_beat.append(
                    beats[-1]
                )
                column_s_quantized.append(
                    gran_map[beats[-1]]
                )
            else:
                # interval_winner = max(
                #     list(overlapping_intervals),
                #     key=lambda interval: MeshScore.get_overlap(s_interval, interval)
                # )

                # let's just use last winner.... what could go wrong?
                column.append(
                    interval_winner.data
                )
                column_beat.append(
                    beats[-1]
                )
                column_s_quantized.append(
                    gran_map[beats[-1]]
                )

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
    def get_gran_map(
            beatmap,
            quantize='16T'
    ):

        gran_map = dict()

        if quantize == '16T':
            num_samples = 49

        for beat, s in enumerate(beatmap[:-1], 0):
            beat_interpolated = np.linspace(beat, beat + 1, num_samples)
            s_interpolated = np.linspace(beatmap[beat], beatmap[beat + 1], num_samples)
            gran_map.update(dict(zip(beat_interpolated, s_interpolated)))

        return gran_map

    # NB: s_beat_start and s_beat_end are determined by human, set via Ableton Live clip end markers
    @staticmethod
    def trim_beatmap(beatmap: List[float], s_beat_start, s_beat_end) -> List[float]:

        s_beat_first_quantized = utils.get_beat_nearest(beatmap, s_beat_start)

        s_beat_last_quantized = utils.get_beat_nearest(beatmap, s_beat_end)

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
            raise Exception('overlap cannot be determined')

    @staticmethod
    def get_struct(obj):
        if type(obj).__name__ == 'Chord':
            return [str(p) for p in obj.pitches]
        elif type(obj).__name__ == 'Note':
            return obj.pitch.midi
        else:
            return obj

    @staticmethod
    def get_interval_tree(df: pd.DataFrame, diff=True, preserve_struct=False) -> IntervalTree:

        struct_last = df.iloc[0].values[0]
        index_struct_last = df.index[0]
        intervals_structs = []

        for row in df.iloc[1:, :].itertuples(index=True, name=True):
            index = row[0]
            struct_current = row[1]

            if not diff:
                intervals_structs.append(
                    Interval(
                        index_struct_last,
                        index,
                        MeshScore.get_struct(struct_last) if not preserve_struct else struct_last
                    )
                )
            else:
                if utils.b_absolutely_equal(struct_current, struct_last):
                    intervals_structs.append(
                        Interval(
                            index_struct_last,
                            index,
                            MeshScore.get_struct(struct_last) if not preserve_struct else struct_last
                        )
                    )

            struct_last = struct_current
            index_struct_last = index

        return IntervalTree(
            Interval(begin, end, data)
            for begin, end, data in intervals_structs
         )

