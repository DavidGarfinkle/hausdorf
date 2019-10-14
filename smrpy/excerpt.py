import sys
import base64
from io import StringIO
import music21
from smrpy import indexers

def coloured_excerpt(symbolic_data, note_list):
    note_list = [int(i) for i in note_list]

    score = music21.converter.parse(symbolic_data)
    nps = list(indexers.NotePointSet(score))
    nps_ids = [nps[i].original_note_id for i in note_list]

    # Get stream excerpt
    _, start_measure = score.beatAndMeasureFromOffset(nps[note_list[0]].offset)
    _, end_measure = score.beatAndMeasureFromOffset(nps[note_list[-1]].offset + nps[note_list[-1]].duration.quarterLength - 1)

    start_measure_num = max(0, start_measure.number - 1)
    last_measure = score.measure(-1)
    if last_measure is not end_measure:
        end_measure_num = end_measure.number + 1
    excerpt = score.measures(numberStart=start_measure_num, numberEnd=end_measure_num)

    # Colour notes
    for note in excerpt.flat.notes:
        if note.id in nps_ids:
            note.style.color = 'red'

    # Delete part names (midi files have bad data)
    for part in excerpt:
        part.partName = ''

    sx = music21.musicxml.m21ToXml.ScoreExporter(excerpt)
    musicxml = sx.parse()

    bfr = StringIO()
    sys.stdout = bfr
    sx.dump(musicxml)
    output = bfr.getvalue()
    sys.stdout = sys.__stdout__

    return output

