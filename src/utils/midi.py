def map_midi(pitch_midi_raw, intervalDesired):
    if intervalDesired:
        if pitch_midi_raw > intervalDesired[1]:
            while (pitch_midi_raw > intervalDesired[1]):
                pitch_midi_raw -= 12
        elif pitch_midi_raw < intervalDesired[0]:
            while (pitch_midi_raw < intervalDesired[0]):
                pitch_midi_raw += 12

    return pitch_midi_raw
