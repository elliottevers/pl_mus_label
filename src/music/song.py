import pandas as pd
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from typing import List, Dict, Any, Optional, Tuple
from music import note

# class Song, or class Mesh


class MeshSong(object):

    data: pd.DataFrame

    def __init__(self):
        self.data = pd.Series([])

    # def add_chords(self, chords: Dict[Any, List[note.MidiNote]], index_type='ms'):
    #     # events_chords: Dict[float, List[note.MidiNote]]
    #     # self.data = pd.merge(self.data, chords, on=index_type)
    #     df_chords = pd.DataFrame(
    #         data={'chords': list(chords.values())}, index=list(chords.keys())
    #     )
    #     df_chords.index.name = index_type

    @staticmethod
    def to_df(chords: Dict[Any, List[note.MidiNote]], index_type='ms'):
        df_chords = pd.DataFrame(
            data={'chords': list(chords.values())}, index=list(chords.keys())
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
        # events_quantized: Dict[float, List[note.MidiNote]] = dict()

        # TODO: add column of beats (NaNs before and after start and end), make it another index
        column_ms_quantized = []
        column_beat = []

        s_beat_first_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - s_beat_start))

        s_beat_last_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - s_beat_end))

        counter = 0
        passed_first_beat = False
        passed_last_beat = False

        index_nearest_s_beat_first_quantized = min(list(s_timeseries.index), key=lambda s_beat: abs(s_beat - s_beat_first_quantized))

        index_nearest_s_beat_last_quantized = min(list(s_timeseries.index), key=lambda s_beat: abs(s_beat - s_beat_last_quantized))

        # figure out index value closest to s_beat_first_quantized
        # figure out index value closest to s_beat_last_quantized

        # s_timeseries.loc[list(s_timeseries.index)[0]]

        for index, row in s_timeseries.iterrows():
            # print(row['c1'], row['c2'])
            if index == index_nearest_s_beat_first_quantized:
                passed_first_beat = True

            if index == index_nearest_s_beat_last_quantized:
                passed_last_beat = True
                counter = 0

            if passed_first_beat and not passed_last_beat:
                counter += 1

            key_s_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - index))

            column_ms_quantized.append(key_s_quantized)
            column_beat.append(counter)

        s_timeseries['ms_quantized'] = column_ms_quantized

        s_timeseries['beat'] = column_beat

        # s_timeseries.reset_index(drop=True, inplace=True)
        #
        # # s_timeseries.drop(['ms'], axis=1, inplace=True)
        #
        # s_timeseries.rename(
        #     {
        #         'ms_quantized': 'ms'
        #     },
        #     inplace=True
        # )
        #
        # # s_timeseries.rename(columns={'ms_quantized': 'ms'}, inplace=True)
        #
        # quantized.set_index(['beat', 'ms'])

        # s_timeseries.sort_index(inplace=True)

        return s_timeseries.reset_index(
            drop=True
        ).rename(
            columns={'ms_quantized': 'ms'}
        ).set_index(
            ['beat', 'ms']
        ).sort_index(
        )

        # s_timeseries.index.name = 'ms'


        # for s, beat in enumerate(column_quantized, 1):
        #     s_timeseries.loc[s] = beat


        # for s, chord in events_chords.items():
        #     key_s_quantized = min(list(beats), key=lambda s_beat: abs(s_beat - s))
        #     events_quantized[key_s_quantized] = chord

        # return

    def add_melody(self, melody: pd.Series, index_type='ms'):
        self.data = pd.merge(self.data, melody, on=index_type)

    # def add_chords(self, chords: Dict[Any, List[note.MidiNote]], index_type='ms'):
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



    # def determine_index(self, ms_list, beat_list, s_beat_start, s_beat_end):
    #     beat_current

    # Dict[
    #     float, List[note.MidiNote]
    # ]:

    def fill_beat_index(beats: List[float], s_beat_start, s_beat_end) -> None:
        events_quantized: Dict[float, List[note.MidiNote]] = dict()

        for s, chord in events_chords.items():
            key_s_quantized = min(list(beats), key=lambda s_beat: abs(s_beat - s))
            events_quantized[key_s_quantized] = chord

        this.data
