import pytest
from convert import vamp as conv_vamp
from live import note as note_live


class TestMonophonify:
    def test_monophonify(self):

        notes_live = [
            note_live.NoteLive(
                pitch=60,
                beat_start=1.8,
                beats_duration=0.5,  # .75 seconds
                velocity=90,
                muted=0
            )
        ]

        # start beat 2.7 seconds - 1.8 in Ableton, 2.8 semantically
        # duration .75 seconds
        # each sample represents .15 seconds

        data_monophonic = conv_vamp.to_data_monophonic(
            notes_live,
            offset_s_audio=0,
            duration_s_audio=6,
            beatmap=[0, 1.5, 3, 4.5, 6],
            sample_rate=float(1 / 10)  # samples per second
        )

        data = data_monophonic['vector'][1]

        # map beat to index [0 => 0, 1.5 => 15, 3 => 30, 4.5 => 45, 6 => 60]

        index_beat_start = 27
        index_beat_end = int(27 + 7.5)

        # what we want: show beat start is at the desired index
        assert data[index_beat_start - 1] == 0
        assert data[index_beat_start] == 60
        assert data[index_beat_start + 1] == 60

        assert data[index_beat_end - 1] == 60
        assert data[index_beat_end] == 0
        assert data[index_beat_end + 1] == 0
