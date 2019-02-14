import pandas as pd
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from typing import List, Dict, Any, Optional, Tuple
from music import note
from convert import midi
# class Song, or class Mesh


class MeshSong(object):

    data: pd.DataFrame

    def __init__(self):
        self.data = pd.Series([])

    # def add_chords(self, chords: Dict[Any, List[note.MidiNote]], index_type='s'):
    #     # events_chords: Dict[float, List[note.MidiNote]]
    #     # self.data = pd.merge(self.data, chords, on=index_type)
    #     df_chords = pd.DataFrame(
    #         data={'chords': list(chords.values())}, index=list(chords.keys())
    #     )
    #     df_chords.index.name = index_type

    @staticmethod
    def to_df(chords: Dict[Any, List[note.MidiNote]], index_type='s'):
        df_chords = pd.DataFrame(
            data={'chord': list(chords.values())}, index=list(chords.keys())
        )
        df_chords.index.name = index_type
        return df_chords

    @staticmethod
    def quantize(
            s_timeseries: pd.DataFrame,
            beatmap: List[float],
            s_beat_start,
            s_beat_end
    ) -> pd.DataFrame:

        # TODO: add column of beats (NaNs before and after start and end), make it another index
        column_s_quantized = []
        column_beat = []

        s_beat_first_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - s_beat_start))

        s_beat_last_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - s_beat_end))

        counter = 0
        passed_first_beat = False
        passed_last_beat = False

        index_nearest_s_beat_first_quantized = min(list(s_timeseries.index), key=lambda s_beat: abs(s_beat - s_beat_first_quantized))

        index_nearest_s_beat_last_quantized = min(list(s_timeseries.index), key=lambda s_beat: abs(s_beat - s_beat_last_quantized))

        for index, row in s_timeseries.iterrows():
            if index == index_nearest_s_beat_first_quantized:
                passed_first_beat = True

            if index == index_nearest_s_beat_last_quantized:
                passed_last_beat = True
                counter = 0

            if passed_first_beat and not passed_last_beat:
                counter += 1

            key_s_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - index))

            column_s_quantized.append(key_s_quantized)
            column_beat.append(counter)

        s_timeseries['s_quantized'] = column_s_quantized

        s_timeseries['beat'] = column_beat

        return s_timeseries.reset_index(
            drop=True
        ).rename(
            columns={'s_quantized': 's'}
        ).set_index(
            ['beat', 's']
        ).sort_index(
        )

    def add_melody(self, melody: pd.DataFrame, index_type='s') -> None:
        self.data = pd.merge(
            self.data.reset_index(),
            melody.reset_index(),
            on=[index_type],
            how='outer'
        ).set_index(
            [index_type, 'beat']
        ).sort_index(
            by=index_type
        )

    # def add_chords(self, chords: Dict[Any, List[note.MidiNote]], index_type='s'):
    #     # events_chords: Dict[float, List[note.MidiNote]]
    #     # self.data = pd.merge(self.data, chords, on=index_type)
    #     df_chords = pd.DataFrame(
    #         data={'chords': list(chords.values())}, index=list(chords.keys())
    #     )
    #     df_chords.index.name = index_type

    def render(self, part_to_track: Dict, type='fixed_tempo') -> MidiFile:
        # add chords to tracks
        return MidiFile()

    def get_time_aligned(self) -> pd.DataFrame:
        return 0

    def get_fixed_tempo(self) -> pd.DataFrame:
        if not self.tempo:
            raise 'tempo estimate not set'
        return 0

