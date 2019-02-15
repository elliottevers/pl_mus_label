from music21 import converter, search, analysis
from subprocess import call as call_shell
import music21

filename_analyze = '/Users/elliottevers/Documents/DocumentsSymlinked/git-repos.nosync/audio/ChordTracks/chords_tswift_tears.mid'

filename_analyze = '/Users/elliottevers/Downloads/ella_chords_test.musicxml'

stream = converter.parse(filename_analyze)

# for part in stream:
#     part.show('text')

# bach = corpus.parse('bwv66.6')
# scoreList = search.segment.indexScoreParts(stream.flat)

# segments, measureLists = search.segment.translateMonophonicPartToSegments(stream)

for note in stream.flat.notes:
    testing = 1
# analyzer = analysis.discrete.BellmanBudge()
#
# wa = analysis.windowed.WindowedAnalysis(stream.flat, analyzer)
#
# solutions, color = wa.analyze(
#     64,  # window_size,  # 64,
#     'overlap'
# )

score = music21.stream.Score()

part_chords = music21.stream.Part()

part_bass = music21.stream.Part()

measure1chords = music21.stream.Measure()

measure2chords = music21.stream.Measure()

measure1notes = music21.stream.Measure()

measure2notes = music21.stream.Measure()

measure1notes.append(
    music21.note.Note(
        pitch='C',
        duration=music21.duration.Duration(2.0)
    )
)

measure1notes.append(
    music21.note.Note(
        pitch='D',
        duration=music21.duration.Duration(2.0)
    )
)

measure2notes.append(
    music21.note.Note(
        pitch='C',
        duration=music21.duration.Duration(2.0)
    )
)

measure2notes.append(
    music21.note.Note(
        pitch='D',
        duration=music21.duration.Duration(2.0)
    )
)

measure1chords.append(
    music21.chord.Chord(
        ['E', 'G'],
        duration=music21.duration.Duration(2.0)
    )
)

measure1chords.append(
    music21.chord.Chord(
        ['F', 'A'],
        duration=music21.duration.Duration(2.0)
    )
)

measure2chords.append(
    music21.chord.Chord(
        ['E', 'G'],
        duration=music21.duration.Duration(2.0)
    )
)

measure2chords.append(
    music21.chord.Chord(
        ['F', 'A'],
        duration=music21.duration.Duration(2.0)
    )
)

part_chords.append(
    measure1chords
)

part_chords.append(
    measure2chords
)

part_bass.append(
    measure1notes
)

part_bass.append(
    measure2notes
)

score.parts.append(
    part_bass
)

score.parts.append(
    part_chords
)

score.insert(0, part_chords)
score.insert(0, part_bass)

# score.show()

segments, measureLists = search.segment.translateMonophonicPartToSegments(score)


# note1 = music21.note.Note('C')


# scoreList[1]['segmentList'][0]
# scoreList[1]['measureList']

# stream.show('midi')

exit(0)


# call_shell(
#     ['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_out]
# )



# import filter.midi as filter
# import convert.midi as midi_convert
# import filter.series as series_filter, filter.midi as midi_filter, analysis_discrete.midi as midi_analysis
# import mido
# import pandas as pd
# import itertools
# import sys
# import music21
# from music21 import converter, graph, analysis
# from mido import MetaMessage
#
# from subprocess import call as call_shell
#
# import seaborn as sns
#
# import matplotlib.pyplot as plt
#
# from subprocess import call as call_shell
#
# # filename_in = '/Users/elliottevers/Downloads/ella_dream_chords.mid'
#
# # filename_out = '/Users/elliottevers/Downloads/ella_dream_chords_doubled.mid'
#
# filename_in = '/Users/elliottevers/Downloads/Chordify_It-Wasn-t-God-Who-Made-Honky-Tonk-Angels-Kitty-Wells_Quantized_at_136_BPM.mid'
#
# filename_out = '/Users/elliottevers/Downloads/kitty_honky_chords_doubled.mid'
#
# # stream = converter.parse(filename_in)
#
# # filename_input = '/Users/elliottevers/Downloads/ella_dream_vocals_2.mid'
#
# # filename_out = '/Users/elliottevers/Downloads/main.mid'
#
# # bounds_graph_percentage = [0, 1]
#
# # size_window = 4000
#
# TRACK_CHORDS = 1  # 1
#
# TRACK_BASS = 2  # 2
#
# bpm_file = 136  # 75
#
# file = mido.MidiFile(filename_in)
#
# ppq = file.ticks_per_beat
#
# track_chords = file.tracks[TRACK_CHORDS]
#
# track_doubled = midi_filter.pad(
#     track_chords,
#     bpm_file,
#     2
# )
#
# file_out = mido.MidiFile(ticks_per_beat=ppq)
#
# file_out.tracks.append(track_doubled)
#
# file_out.save(filename_out)
#
# # call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_out])
#
# # exit(0)
#
# filename_in = '/Users/elliottevers/Downloads/kitty_honky_chords_doubled.mid' # '/Users/elliottevers/Downloads/ella_dream_chords_doubled.mid'
#
# stream = converter.parse(filename_in)
#
# # solutions = midi_analysis.key_center_windowed_complete(
# #     part=stream,
# #     window_size_measures=64,
# #     melody=True
# # )
#
# analyzer = analysis.discrete.BellmanBudge()
# #
# wa = analysis.windowed.WindowedAnalysis(stream.parts[0], analyzer)
# #
#
# window_size = 256
#
# solutions, color = wa.analyze(
#     window_size,  # 64,
#     'overlap'
# )
#
# # (len(solutions) + 64 - 1)/2
#
# # have to determine number of measures automatically
#
# num_measures = (len(solutions) + window_size - 1)/2  # 230
#
# notes = []
#
# solutions = [tuple_pitch[0].midi for tuple_pitch in solutions]
#
# for i_measure in range(1, int(num_measures)):
#     notes.append(solutions[i_measure])
#
# # [tuple_pitch[0].midi for tuple_pitch in solutions]
#
# # solutions_hardcoded = [60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 60, 60, 60, 60, 60, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 65, 65, 70, 70, 70, 70, 70, 70, 70, 70, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60]
#
# # generate midi track of tones
#
# # figure out how many ticks to make each note - ppq of track to "overdub"
#
# # listen to track together for validation
#
# file_overdubbed = mido.MidiFile(ticks_per_beat=ppq)
#
# track_main = track_chords
#
# track_overdub = mido.MidiTrack()
#
# track_overdub.append(
#     MetaMessage(
#         'time_signature',
#         time=0
#     )
# )
#
# track_overdub.append(
#     MetaMessage(
#         'set_tempo',
#         tempo=mido.bpm2tempo(bpm_file),
#         time=0
#     )
# )
#
# velocity = 90
#
# for pitch_midi in solutions:
#     track_overdub.append(
#         mido.Message(
#             'note_on',
#             note=pitch_midi,
#             velocity=velocity,
#             time=0
#         )
#     )
#     track_overdub.append(
#         mido.Message(
#             'note_off',
#             note=pitch_midi,
#             velocity=0,
#             time=ppq
#         )
#     )
#
# file_overdubbed.tracks.append(track_main)
#
# file_overdubbed.tracks.append(track_overdub)
#
# filename_out = '/Users/elliottevers/Downloads/kitty_honky_chords_and_key_centers.mid'
#
# file_overdubbed.save(filename_out)
#
# call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_out])
#
# # print(notes)
#
# exit(0)
#
# df = midi_convert.mid_to_series(
#     file.tracks[2]
# )
#
# df_padded = df.append(df, ignore_index=True).append(df, ignore_index=True).append(df, ignore_index=True)
#
# track = midi_convert.series_to_mid(
#     df_padded,
#     90
# )
#
# file_out = mido.MidiFile()
#
# file_out.tracks.append(track)
#
# file_out.save(filename_out)
#
# call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_out])
#
# # call_shell(['open', '-a', '/Applications/MidiYodi 2018.1.app/', filename_in])
#
# exit(0)
#
# # p = graph.plot.WindowedKey(stream.parts[0])
# #
# # p.processorClass = analysis_discrete.discrete.BellmanBudge
#
# # p.doneAction = 'show'
#
# # p.run()
#
# # solutions = p.processor.solutionsFound
#
# # testing = 1
#
# analyzer = analysis.discrete.BellmanBudge()
#
# wa = analysis.windowed.WindowedAnalysis(stream.parts[0], analyzer)
#
# # create pandas series, turn into midi using convert
#
# # specifications
#
# # parameters - choose quarter length
#
# # at that granularity, create track of of key center sequence
#
# # solutions, colors, meta = wa.process(
# #     minWindow=2,
# #     maxWindow=2,
# #     windowStepSize=64,
# #     windowType='adjacentAverage',
# #     includeTotalWindow=False
# # )
#
# # 64 seems to work well
# solutions, color = wa.analyze(
#     64,
#     'overlap'
# )
#
# testing = 1
