from unittest import TestCase
import mido
from subprocess import call as call_shell
import pandas as pd
import convert.midi as midi_convert


class TestMid_to_series(TestCase):
    def test_mid_to_series(self):
        file = mido.MidiFile(ticks_per_beat=2)

        track1 = mido.MidiTrack()

        file.tracks.append(track1)

        track1.append(
            mido.MetaMessage(
                'set_tempo',
                tempo=500000 * 2 * 2
            )
        )

        track2 = mido.MidiTrack()

        file.tracks.append(track2)

        track2.append(
            mido.MetaMessage(
                'set_tempo',
                tempo=500000 * 2 * 2
            )
        )

        track3 = mido.MidiTrack()

        file.tracks.append(track3)

        track3.append(
            mido.MetaMessage(
                'set_tempo',
                tempo=500000 * 2 * 2
            )
        )

        track4 = mido.MidiTrack()

        file.tracks.append(track4)

        track4.append(
            mido.MetaMessage(
                'set_tempo',
                tempo=500000 * 2 * 2
            )
        )

        track1.append(
            mido.Message(
                'note_on',
                note=60,
                velocity=90,
                time=0
            )
        )

        track1.append(
            mido.Message(
                'note_off',
                note=60,
                velocity=0,
                time=1
            )
        )

        track1.append(
            mido.Message(
                'note_on',
                note=67,
                velocity=90,
                time=1
            )
        )

        track1.append(
            mido.Message(
                'note_off',
                note=67,
                velocity=0,
                time=1
            )
        )

        track2.append(
            mido.Message(
                'note_on',
                note=60,
                velocity=90,
                time=0
            )
        )

        track2.append(
            mido.Message(
                'note_off',
                note=60,
                velocity=0,
                time=1
            )
        )

        track2.append(
            mido.Message(
                'note_on',
                note=67,
                velocity=90,
                time=0
            )
        )

        track2.append(
            mido.Message(
                'note_off',
                note=67,
                velocity=0,
                time=2
            )
        )

        track3.append(
            mido.Message(
                'note_on',
                note=60,
                velocity=90,
                time=0
            )
        )

        track3.append(
            mido.Message(
                'note_on',
                note=67,
                velocity=90,
                time=1
            )
        )

        track3.append(
            mido.Message(
                'note_off',
                note=60,
                velocity=0,
                time=1
            )
        )

        track3.append(
            mido.Message(
                'note_off',
                note=67,
                velocity=0,
                time=1
            )
        )

        track4.append(
            mido.Message(
                'note_on',
                note=60,
                velocity=90,
                time=0
            )
        )

        track4.append(
            mido.Message(
                'note_on',
                note=67,
                velocity=90,
                time=1
            )
        )

        track4.append(
            mido.Message(
                'note_off',
                note=67,
                velocity=0,
                time=1
            )
        )

        track4.append(
            mido.Message(
                'note_off',
                note=60,
                velocity=0,
                time=1
            )
        )

        # filename_out = '/Users/elliottevers/Downloads/simulated_data.mid'

        # file.save(filename_out)

        # call_shell(["open", "-a", "/Applications/MidiYodi 2018.1.app/", filename_out])

        # exit(0)

        # case 1

        gt1 = pd.Series(
            [60, None, 67, None],
            index=list(range(0, 4))
        )

        gt2 = pd.Series(
            [60, 67, 67, None],
            index=list(range(0, 4))
        )

        gt3 = pd.Series(
            [60, 67, 67, None],
            index=list(range(0, 4))
        )

        gt4 = pd.Series(
            [60, 67, 60, None],
            index=list(range(0, 4))
        )


        gt5 = {
            60: [0, 1],
            67: [2, 3]
        }


        # gt6 = pd.Series(
        #     [60, 67, 67, None],
        #     index=list(range(0, 4))
        # )

        gt6 = {
            60: [0, 1],
            67: [1, 3]
        }

        # gt7 = pd.Series(
        #     [60, 67, 67, None],
        #     index=list(range(0, 4))
        # )

        gt7 = {
            60: [0, 2],
            67: [1, 3]
        }

        # gt8 = pd.Series(
        #     [60, 67, 60, None],
        #     index=list(range(0, 4))
        # )

        gt8 = {
            60: [1, 2],
            67: [0, 3]
        }


        result1 = midi_convert.mid_to_series(file.tracks[0])[0]

        result2 = midi_convert.mid_to_series(file.tracks[1])[0]

        result3 = midi_convert.mid_to_series(file.tracks[2])[0]

        result4 = midi_convert.mid_to_series(file.tracks[3])[0]


        result5 = midi_convert.mid_to_series(file.tracks[0])[1]

        result6 = midi_convert.mid_to_series(file.tracks[1])[1]

        result7 = midi_convert.mid_to_series(file.tracks[2])[1]

        result8 = midi_convert.mid_to_series(file.tracks[3])[1]

        # thing1 = pd.Series(
        #     [4, 5, 6],
        #     index=[1, 2, 3]
        # )
        #
        # thing2 = pd.Series(
        #     [4, 5, 6],
        #     index=[1, 2, 3]
        # )

        # assert thing1.equals(thing2)

        assert result1.equals(gt1)
        assert result2.equals(gt2)
        assert result3.equals(gt3)
        assert result4.equals(gt4)

        # assert result5.equals(gt5)
        # assert result6.equals(gt6)
        # assert result7.equals(gt7)
        # assert result8.equals(gt8)
