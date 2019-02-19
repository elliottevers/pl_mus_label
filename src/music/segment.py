

class SegmentNoteMapper(object):
    # TODO: assumes there will only ever be two overlapping segments at maximum
    note_mapping = dict()
    segments = set()

    def __init__(self):
        self.pitches = {60, 72}

    def _get_remaining_notes(self):
        return self.pitches.difference(set(list(self.note_mapping.values())))

    def add(self, segments_encountered: set):
        # out with the old
        for segment in self.segments:
            if not segment in segments_encountered:
                del self.note_mapping[segment]

        # in with the new
        for segment in segments_encountered:
            if not segment in self.segments:
                self.note_mapping[segment] = list(self._get_remaining_notes())[0]

        self.segments = segments_encountered

    def get_current_pitches(self):
        return list(self.note_mapping.values())

    @staticmethod
    def get_segments_overlapping(index_measure, measure_lists, segments) -> set:
        segments_overlapping = []

        for i_measure, interval_measure in enumerate(measure_lists):
            if interval_measure[0] <= index_measure <= interval_measure[1]:
                segments_overlapping.append(segments[i_measure])

        return set(segments_overlapping)
