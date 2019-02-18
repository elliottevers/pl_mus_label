from typing import List, Dict, Any, Optional, Tuple


class NoteLive(object):

    @staticmethod
    def parse_list(
            list_notes
    ):
        notes = []
        for i_note, note in enumerate(list_notes, 1):
            if i_note == 1:
                continue
            if i_note == len(list_notes):
                continue
            notes.append(NoteLive.parse(note.split(' ')))

        return notes

    @staticmethod
    def parse(
            list_note: List[int]
    ):
        return NoteLive(
            pitch=int(list_note[0]),
            beat_start=int(list_note[1]),
            beats_duration=int(list_note[2]),
            velocity=int(list_note[3]),
            muted=int(list_note[4])
        )

    def __init__(
            self,
            pitch: int,
            beat_start: int,
            beats_duration: int,
            velocity: int,
            muted: int
    ):
        self.pitch = pitch
        self.beat_start = beat_start
        self.beats_duration = beats_duration
        self.velocity = velocity
        self.muted = muted

    def encode(self):
        return ' '.join([
            str(self.pitch),
            str(self.beat_start),
            str(self.beats_duration),
            str(self.velocity),
            str(self.muted)
        ])

        # constructor(
        #     pitch: number,
        #     beat_start: number,
        #     beats_duration: number,
        #     velocity: number,
        #     muted: number
        # ) {
        #     this.pitch = Number(pitch);
        #     this.beat_start = Number(beat_start);
        #     this.beats_duration = Number(beats_duration);
        #     this.velocity = Number(velocity);
        #     this.muted = Number(muted);
        #     this._b_has_chosen = false;
        # }


# def parse(list: List[int]):

# [ 72, 0, 1, 80, 0 ]