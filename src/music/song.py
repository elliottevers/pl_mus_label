import pandas as pd
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from typing import List, Dict, Any, Optional, Tuple
from music import note, chord
from convert import midi as convert_midi
from intervaltree import IntervalTree, Interval
import music21
import math
import numpy as np


class MeshSong(object):

    tree_melody: IntervalTree

    tree_chords: IntervalTree

    tree_key_centers: IntervalTree

    tree_bass: IntervalTree

    tree_segments: IntervalTree

    data: pd.DataFrame

    def __init__(self):
        self.data = None

    # def add_chords(self, chords: Dict[Any, List[note.MidiNote]], index_type='s'):
    #     # events_chords: Dict[float, List[note.MidiNote]]
    #     # self.data = pd.merge(self.data, chords, on=index_type)
    #     df_chords = pd.DataFrame(
    #         data={'chords': list(chords.values())}, index=list(chords.keys())
    #     )
    #     df_chords.index.name = index_type

    def add_quantization(self):
        return 0

    @staticmethod
    # def chords_to_df(chords: Dict[Any, List[note.MidiNote]], index_type='s'):
    def chords_to_df(chords: Dict[Any, chord.ChordMidi], index_type='s'):
        df_chords = pd.DataFrame(
            data={'chord': list(chords.values())}, index=list(chords.keys())
        )

        df_chords.index.name = index_type

        return df_chords

    @staticmethod
    def segments_to_df(data_segments, index_type='s'):

        segments = [
            {
                'timestamp': segment['timestamp'],
                'duration': segment['duration']
            }

            for segment
            in data_segments
        ]

        df_segments = pd.DataFrame(
            data={
                'segment': [
                    note.MidiNote(
                        pitch=60,
                        duration_ticks=convert_midi.s_to_ticks(segment['duration']),  # TODO: make sure defaults (bpm, ppq) don't fuck with this
                        velocity=90,
                        channel=10,
                        program=49
                    )
                    for segment
                    in segments
                ]
            },
            index=[
                segment['timestamp'] for segment in segments
            ]
        )

        df_segments.index.name = index_type

        return df_segments

    @staticmethod
    def melody_to_df(data_melody, index_type='s'):
        list_melody = data_melody[1]

        sample_rate = data_melody[0]

        df_melody_hz = pd.DataFrame(
            data={'melody': list_melody},
            index=[i_sample * sample_rate for i_sample, sample in enumerate(list_melody)]
        )

        df_melody_hz.index.name = index_type

        return df_melody_hz

    # TODO: put somewhere else
    @staticmethod
    def get_note(pitch_midi):
        if not pitch_midi or math.isinf(pitch_midi) or math.isnan(pitch_midi) or pitch_midi == 0:
            return None
        else:
            return music21.note.Note(pitch=music21.pitch.Pitch(midi=int(pitch_midi)))

    # def set_melody_tree_attempt_1(self) -> None:
    #     # iterate over s index
    #     # look for changes
    #     melody_last = self.data.loc[self.data.index[0], :].values[1]
    #     index_melody_last = self.data.index[0]
    #     intervals_melody = []
    #
    #     for i, (i_full, row) in enumerate(self.data.iloc[1:, :].iterrows()):
    #         melody_current = row['melody']
    #         row_last = self.data.loc[(i_full[0] - 1, slice(None), slice(None))]
    #         melody_last = row_last.values[0][1]
    #         if melody_current != melody_last:
    #             intervals_melody.append(
    #                 Interval(
    #                     index_melody_last[1],
    #                     i_full[1],
    #                     MeshSong.get_note(melody_last)
    #                 )
    #             )
    #             melody_last = melody_current
    #             index_melody_last = i_full
    #
    #     self.tree_melody = IntervalTree(
    #         Interval(begin, end, data)
    #         for begin, end, data in intervals_melody
    #      )

    # def set_melody_tree_attempt_2(self) -> None:
    #     # iterate over s index
    #     # look for changes
    #     # melody_last = self.data.loc[self.data.index[0], :].values[1]
    #     # index_melody_last = self.data.index[0]
    #     # intervals_melody = []
    #
    #     # index_list = self.data.index.tolist()
    #
    #     melody_last = self.data.loc[(0, slice(None), slice(None)), 'melody']
    #     index_melody_last = (0, slice(None), slice(None))
    #     intervals_melody = []
    #
    #     for row in self.data.iloc[1:, :].itertuples(index=True, name=True):
    #         index = row[0]
    #         melody_current = row[2]
    #         # TODO: do this without looking up the last row
    #         # row_last = self.data.loc[(index[0] - 1, slice(None), slice(None))]
    #         # melody_last = row_last.values[0][1]
    #         # TODO: put back in
    #         # if melody_current != melody_last:
    #         #     intervals_melody.append(
    #         #         Interval(
    #         #             index_melody_last[1],
    #         #             index[1],
    #         #             MeshSong.get_note(melody_last)
    #         #         )
    #         #     )
    #         #     melody_last = melody_current
    #         #     index_melody_last = index
    #
    #     self.tree_melody = IntervalTree(
    #         Interval(begin, end, data)
    #         for begin, end, data in intervals_melody
    #      )

    @staticmethod
    def get_gran_map(beatmap, quantize='16T'):

        gran_map = dict()

        if quantize == '16T':
            num_samples = 49

        for beat, s in enumerate(beatmap[:-1], 1):
            index_beatmap = beat - 1
            beat_interpolated = np.linspace(beat, beat + 1, num_samples)
            s_interpolated = np.linspace(beatmap[index_beatmap], beatmap[index_beatmap + 1], num_samples)
            gran_map.update(dict(zip(beat_interpolated, s_interpolated)))

        return gran_map

    # NB: s_beat_start and s_beat_end are determined by human
    def trim_beatmap(self, beatmap: List[float], s_beat_start, s_beat_end) -> List[float]:

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

    def _get_maximum_overlap(self, gran_map):

        column_s_quantized = []
        column_beat = []
        column_melody = []

        beats = sorted(list(gran_map.keys()))
        # endpoint_beat_last = beats[0]
        endpoint_s_last = sorted(list(gran_map.values()))[0]

        for beat in beats[:-1]:

            s = gran_map[beat]

            s_interval = (endpoint_s_last, s)

            intervals_melody_overlaps = self.tree_melody.overlap(
                s_interval[0],
                s_interval[1]
            )

            if len(list(intervals_melody_overlaps)) < 1:
                column_melody.append(
                    None
                )
                column_beat.append(
                    beat
                )
                column_s_quantized.append(
                    s
                )
            else:
                interval_winner = max(list(intervals_melody_overlaps), key=lambda melody_interval: MeshSong.get_overlap(s_interval, melody_interval))

                column_melody.append(
                    interval_winner.data
                )
                column_beat.append(
                    beat
                )
                column_s_quantized.append(
                    s
                )

            # endpoint_beat_last = beat
            endpoint_s_last = s

        return pd.DataFrame(
            data={
                'melody': column_melody,
                'beat': column_beat,
                's': column_s_quantized
            }
        ).set_index(
            ['beat', 's']
        ).sort_index(
        )

    def _quantize(self, beatmap, s_beat_start, s_beat_end):

        gran_map = MeshSong.get_gran_map(self.trim_beatmap(beatmap, s_beat_start, s_beat_end))

        return self._get_maximum_overlap(gran_map)

    def set_melody_tree(self, melody) -> None:

        midi_last = melody.iloc[0].values[0]
        index_midi_last = melody.index[0]
        intervals_melody = []
        index_last = melody.index[0]

        for row in melody.iloc[1:, :].itertuples(index=True, name=True):
            index = row[0]
            midi_current = row[1]
            if midi_current != midi_last:
                if index_last > index_midi_last:
                    intervals_melody.append(
                        Interval(
                            index_midi_last,
                            index_last,
                            MeshSong.get_note(midi_current)
                        )
                    )
                midi_last = midi_current
                index_midi_last = index
            index_last = index

        self.tree_melody = IntervalTree(
            Interval(begin, end, data)
            for begin, end, data in intervals_melody
         )

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
        column_chord = []

        s_beat_first_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - s_beat_start))

        s_beat_last_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - s_beat_end))

        i_beat_first = beatmap.index(s_beat_first_quantized)

        # def within_inveral(candidate: float, interval: Tuple):
        #     return interval[0] <= candidate <= interval[1]

        from intervaltree import Interval, IntervalTree

        intervals_chords = []

        list_index = s_timeseries.index.tolist()

        for i_ms, ms in enumerate(list_index[:-1]):
            intervals_chords.append(
                (
                    ms,
                    list_index[i_ms + 1],
                    s_timeseries.loc[list_index[i_ms]]['chord']
                )
            )

        intervals_chords.append(
            (
                list_index[-1],
                list_index[-1] + 100, # TODO: we need to use the length of the song to determine when to cutoff the last chord
                s_timeseries.loc[list_index[-1]]['chord']
            )
        )

        interval_tree_chords = IntervalTree(
            Interval(begin, end, data)
            for begin, end, data in intervals_chords
         )

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

        for i_beat, s_beat in enumerate(beatmap[:-1]):

            beat_interval = (beatmap[i_beat], beatmap[i_beat + 1])

            intervals_chords_overlaps = interval_tree_chords.overlap(
                beat_interval[0],
                beat_interval[1]
            )

            # TODO: get element of intervals_chords with highest score according to get_overlap()

            if len(list(intervals_chords_overlaps)) < 1:
                column_chord.append(
                    None
                )
                column_beat.append(
                    i_beat - i_beat_first + 1
                )
                column_s_quantized.append(
                    s_beat
                )
            else:
                interval_winner = max(list(intervals_chords_overlaps), key=lambda chord_interval: get_overlap(beat_interval, chord_interval))

                # beat_to_candidate_key_map[i_beat] = candidate_keys
                column_chord.append(
                    interval_winner.data
                )
                column_beat.append(
                    i_beat - i_beat_first + 1
                )
                column_s_quantized.append(
                    s_beat
                )

        return pd.DataFrame(
            data={
                'chord': column_chord,
                'beat': column_beat,
                's': column_s_quantized
            }
        ).set_index(
            ['beat', 's']
        ).sort_index(
        )

    # @staticmethod
    # def quantize(
    #         s_timeseries: pd.DataFrame,
    #         beatmap: List[float],
    #         s_beat_start,
    #         s_beat_end
    # ) -> pd.DataFrame:
    #
    #     # TODO: add column of beats (NaNs before and after start and end), make it another index
    #     column_s_quantized = []
    #     column_beat = []
    #
    #     s_beat_first_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - s_beat_start))
    #
    #     s_beat_last_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - s_beat_end))
    #
    #     counter = 0
    #     passed_first_beat = False
    #     passed_last_beat = False
    #
    #     index_nearest_s_beat_first_quantized = min(list(s_timeseries.index), key=lambda s_beat: abs(s_beat - s_beat_first_quantized))
    #
    #     index_nearest_s_beat_last_quantized = min(list(s_timeseries.index), key=lambda s_beat: abs(s_beat - s_beat_last_quantized))
    #
    #     for index, row in s_timeseries.iterrows():
    #         if index == index_nearest_s_beat_first_quantized:
    #             passed_first_beat = True
    #
    #         if index == index_nearest_s_beat_last_quantized:
    #             passed_last_beat = True
    #             counter = 0
    #
    #         if passed_first_beat and not passed_last_beat:
    #             counter += 1
    #
    #         key_s_quantized = min(list(beatmap), key=lambda s_beat: abs(s_beat - index))
    #
    #         column_s_quantized.append(key_s_quantized)
    #
    #         # find position, wrt first beat, of closest
    #         column_beat.append(
    #             # counter
    #             beatmap.index(key_s_quantized) - beatmap.index(s_beat_first_quantized) + 1
    #         )
    #
    #     s_timeseries['s_quantized'] = column_s_quantized
    #
    #     s_timeseries['beat'] = column_beat
    #
    #     # TODO: indices should *not* be from chord estimate, but from beat map - chord estimate is used to assign chord at user specified granulatiry
    #     return s_timeseries.reset_index(
    #         drop=True
    #     ).rename(
    #         columns={'s_quantized': 's'}
    #     ).set_index(
    #         ['beat', 's']
    #     ).sort_index(
    #     )

    def render(self, part_to_track: Dict, type='fixed_tempo') -> MidiFile:
        # add chords to tracks

        # for column in self.data.columns:
        #     for i_
        return MidiFile()

    def create_notes(self, index='melody'):

        raise 'not implemented'

    def quantize_on_index(self, index='beat', granularity='16T'):
        # assigns to each 'ms' index, a corresponding 'beat' index
        # quantizes entire df based on index
        raise 'not implemented'

    def fill_legato(self, name_column='chord') -> None:
        col_legato = []
        struct_current = None
        for chord in self.data['chord'].tolist():
            testing = 1

    def add_pk(self):
        column_pk = [i for i in range(len(self.data))]
        self.data['pk'] = column_pk
        self.data.reset_index(
            inplace=True
        )
        self.data.set_index(
            ['pk', 's', 'beat'],
            inplace=True
        )
        self.data.sort_index(
            by='s',
            inplace=True
        )

    # TODO: support index type 's' (melodyne) and 'beat' (trascription after source separation)
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

    def add_chords(self, chords: pd.DataFrame, index_type='s') -> None:
        if not self.data:
            self.data = chords
        else:
            self.data = pd.merge(
                self.data.reset_index(),
                chords.reset_index(),
                on=[index_type],
                how='outer'
            ).set_index(
                [index_type, 'beat']
            ).sort_index(
                by=index_type
            )

    def add_segments(self, segments: pd.DataFrame, index_type='s') -> None:
        self.data = pd.merge(
            self.data.reset_index(),
            segments.reset_index(),
            on=[index_type],
            how='outer'
        ).set_index(
            [index_type, 'beat']
        ).sort_index(
            by=index_type
        )

    def add_bass(self, bass: pd.DataFrame, index_type='s') -> None:
        self.data = pd.merge(
            self.data.reset_index(),
            bass.reset_index(),
            on=[index_type, 'beat'],
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

    def get_time_aligned(self) -> pd.DataFrame:
        return 0

    def get_fixed_tempo(self) -> pd.DataFrame:
        if not self.tempo:
            raise 'tempo estimate not set'
        return 0

# import mido
# from mido import Message, MidiFile, MidiTrack, MetaMessage
# from music21 import stream as stream21, note as note21, pitch as pitch21, duration as duration21
# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# import convert.series_to_mid as series2mid
# import music21
# import os
# import importlib
#
# sns.set(style="darkgrid")
#
# # importlib.import_module(os.path.dirname(os.path.realpath(mido.__file__)) + '/midifiles/midifiles.py')
#
# # mido, midifiles.py
#
# DEFAULT_TEMPO = 500000
#
# filename_input = '/Users/elliottevers/Downloads/ella_dream_vocals_2.mid'
#
# filename_output = '/Users/elliottevers/Downloads/output_midi_to_ticks_timeseries.mid'
#
# program_change = 22  # harmonica
#
# file = MidiFile(filename_input)
#
# ticks_per_beat = file.ticks_per_beat
#
# ppq = ticks_per_beat
#
# mid = MidiFile(ticks_per_beat=ticks_per_beat)
# track = MidiTrack()
# mid.tracks.append(track)
#
# track.append(
#     Message(
#         'program_change',
#         program=program_change,
#         time=0
#     )
# )
#
# iter_tick = 0
#
# tick_last = 0
#
# ticks = []
#
# notes_midi = []
#
# bpm = mido.tempo2bpm(DEFAULT_TEMPO)
#
# track.append(
#     MetaMessage(
#         'time_signature',
#         time=0
#     )
# )
#
# track.append(
#     MetaMessage(
#         'set_tempo',
#         tempo=mido.bpm2tempo(bpm),
#         time=0
#     )
# )
#
# stream = stream21.Stream()
#
# thing = []
#
# for msg in file:
#
#     if msg.type == 'note_on':
#         # assert len(thing) == 0  # monophonic
#
#         ticks_since_onset_last = int(round(mido.second2tick(msg.time, ticks_per_beat, mido.bpm2tempo(bpm))))
#         track.append(Message('note_on', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
#         # quarter note in ticks - ticks_since_onset_last/ticks_per_beat
#         # duration = duration21.Duration()
#         # duration.quarterLength = ticks_since_onset_last/ticks_per_beat
#
#         pitch = pitch21.Pitch()
#         pitch.midi = msg.note
#
#         note = note21.Note()
#         # note.duration = duration
#         note.pitch = pitch
#
#         # stream.append(note)
#         thing.append(note)
#
#         for tick_empty in range(ticks_since_onset_last):
#             iter_tick += 1
#             ticks.append(tick_last + tick_empty)
#             notes_midi.append(None)
#
#     if msg.type == 'note_off':
#         # assert len(thing) == 1  # monophonic
#
#         ticks_since_onset_last = int(round(mido.second2tick(msg.time, ticks_per_beat, mido.bpm2tempo(bpm))))
#         track.append(Message('note_off', note=msg.note, velocity=msg.velocity, time=ticks_since_onset_last))
#
#         duration = duration21.Duration()
#         duration.quarterLength = ticks_since_onset_last / ticks_per_beat
#
#         note = thing.pop()
#
#         note.duration = duration
#
#         stream.append(note)
#
#         # pitch = pitch21.Pitch()
#         # pitch.midi = msg.note
#         #
#         # note = note21.Note()
#         # note.duration = duration
#         # note.pitch = pitch
#         #
#         # stream.append(note)
#
#         for tick in range(ticks_since_onset_last):
#             iter_tick += 1
#             ticks.append(tick_last + tick)
#             notes_midi.append(msg.note)
#
#     tick_last = iter_tick
#
#
# # TODO: we're trying to convert to music21 object here - this also might be the key to making monophonic midi file
#
# df = pd.Series(
#     notes_midi,
#     index=np.array(ticks)
# )
#
#
# mid2 = MidiFile(ticks_per_beat=ticks_per_beat)
#
# track2 = MidiTrack()
#
# mid2.tracks.append(
#     series2mid.timeseries_ticks_to_mid(
#         df,
#         track2,
#         90
#     )
# )
#
# lim = int(round(len(df.index)/4))
#
# sns.relplot(kind="line", data=df[1:lim])
#
#
# plt.show()
#
#
# # df.plot()
#
# # stream.plot()
# mid2.save(filename_output)

