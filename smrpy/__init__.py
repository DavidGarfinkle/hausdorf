import ast
import base64
import music21
import urllib.parse
import xml.etree.ElementTree as ET
import io
from itertools import combinations
from collections import namedtuple
from smrpy.indexers import NotePointSet, m21_xml
from smrpy.piece import Piece, Note, NoteWindow
from smrpy.hausdorf import generate_normalized_windows_with_notes
from smrpy.excerpt import coloured_excerpt

try:
    import plpy
except ImportError:
    plpy = False
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

def log(msg):
    if plpy:
        plpy.warning(msg)
    else:
        logger.debug(msg)

def plpy_execute(query, types, values):
    assert query.count('%s') == len(types)
    assert len(types) == len(values)
    
    for i in range(len(values)):
        query = query.replace('%s', '$' + str(i + 1), 1)

    plan = plpy.prepare(query, types)
    return plpy.execute(plan, values)

def index_piece(pg_id, data):
    # todo make this a transaction
    posting_query = """
        INSERT INTO Posting (n, pid, u, v, nid)
        VALUES (%s, %s, %s, %s, %s)
    """
    p = Piece(data)
    plpy_execute("UPDATE Piece SET music21_xml=%s WHERE pid=%s", ("text", "integer"), (p.data, pg_id))

    for n in p.notes:
        plpy_execute(*(n.insert_str(pg_id)))

    for (u, v), normalized_window, window in generate_normalized_windows_with_notes(p.notes, 10):
        plpy_execute(
                "INSERT INTO NoteWindow(pid, u, v, normalized, unnormalized) VALUES (%s, %s, %s, %s, %s)",
                ("integer", "integer", "integer", "point[]", "point[]"),
                (pg_id, u.index, v.index, [(n.onset, n.pitch) for n in normalized_window], [(n.onset, n.pitch) for n in window]))
        for i, n in enumerate(normalized_window):
            plpy_execute(posting_query, ("point", "integer", "integer", "integer", "integer"),
                ((n.onset, n.pitch), pg_id, u.index, v.index, n.index))

def notes_from_input(inp):
    import json
    point_array = json.loads(inp)
    return [Note(p['x'], None, p['y'], i) for i, p in enumerate(point_array)]

def notes_from_points(inp):
    tuple_list = map(lambda string_tuple: ast.literal_eval(string_tuple), inp)
    return [Note(p[0], None, p[1], i) for i, p in enumerate(tuple_list)]

PostingKey = namedtuple('PostingKey', ['pid', 'u', 'v'])

"""
WITH
pattern_notes AS (SELECT unnest('{"(0,0)","(0,4)","(0,9)","(0,12)","(1,-2)","(1,5)","(1,10)","(1,14)"}'::POINT[]) AS n),
postings AS (
        SELECT Note.n, Note.pid, Note.nid, Posting.u, Posting.v
        FROM Posting JOIN Note ON Note.pid = Posting.pid AND Note.nid = Posting.nid
        JOIN pattern_notes ON Posting.n ~= pattern_notes.n
        ORDER BY (Note.pid, Posting.u, Posting.v, Note.nid) ASC)
SELECT DISTINCT ON (nids) array_agg(postings.n) AS notes, postings.pid, array_agg(postings.nid) AS nids, postings.u, postings.v
FROM postings
GROUP BY (postings.pid, postings.u, postings.v)
HAVING COUNT(postings.n) = 7;
"""

"""
def search(query):
    notes = notes_from_points(query)
    m = []
    for (u, v), window in generate_normalized_windows_with_notes(notes, len(notes)):
        matches = {}
        for pattern_note in window:
            postings = plpy_execute("
                SELECT Note.n WHERE Note.nid = Posting.u
                SELECT Note.n, Note.pid, Note.nid, Posting.u, Posting.v
                FROM Posting JOIN Note ON Note.pid = Posting.pid AND Note.nid = Posting.nid
                WHERE Posting.n ~= %s",
                ("point",), ((pattern_note.onset, pattern_note.pitch),))
            for posting in postings:
                original_note, pid, nid, u, v = posting["n"], posting["pid"], posting["nid"], posting["u"], posting["v"]
                key = PostingKey(pid, u, v)
                matches[key] = matches.get(key, ((u, 0),)) + ((nid, original_note, pattern_note.index),)
        m.append(matches)
    res = set((key.pid, c[key]) for c in m for key in c if len(c[key]) == len(notes))
    pg_results = ([{"pid": k, "nids": [t[0] for t in v], "notes": [t[1] for t in v]} for k, v in res])
    return pg_results
"""

def search(query):
    m = set()
    notes = [Note.from_point(i, p) for i, p in enumerate(points)]
    for nw in NoteWindow.from_notes(pid, notes, window_size):
        results = plpy.execute(f"""
            SELECT search_sql_gin_exact('{nw.to_string}')
        """)
        for r in results:
            if filter_occurrence(query, r['notes'], len(r['notes']), range(-12, 12), 0, 0):
                m += tuple(r.items())
    return m

def filter_occurrence(query_points, occ_points, threshold, transpositions, intervening, inexact):
    return (
        len(points) >= threshold and \
        (query_points[0][1] - points[0][1]) % 12 in transpositions)


def excerpt(pid, nids):
    symbolic_data_query = "SELECT music21_xml FROM Piece WHERE pid=%s"
    symbolic_data, = plpy_execute(symbolic_data_query, ("integer",), (pid,))
    return coloured_excerpt(symbolic_data['music21_xml'], nids)

def generate_notewindows(points, window_size, pid=-1):
    notes = [Note.from_point(i, p) for i, p in enumerate(points)]
    for nw in NoteWindow.from_notes(pid, notes, window_size):
        #yield (nw.pid, nw.notes[0].onset, nw.notes[-1].onset, nw.u.index, nw.v.index, [n.to_point() for n in nw.notes], [n.to_point() for n in nw.normalized_notes]) 
        yield {
            'pid': nw.pid,
            'u': nw.u.index,
            'v': nw.v.index,
            'onset_start': nw.notes[0].onset,
            'onset_end': nw.notes[-1].onset,
            'unnormalized': [n.to_point() for n in nw.notes],
            'normalized': [n.to_point() for n in nw.normalized_notes]
        }

def symbolic_data_to_m21_xml(sd_b64):
    sd = base64.b64decode(sd_b64)
    stream = music21.converter.parse(sd)
    xml = m21_xml(stream)
    return xml.decode('utf-8')

def excerpt(m21_xml, notes, color='#FF0000'):
    smrpy_notes = [Note.from_point(-1, n) for n in notes]
    root = ET.fromstring(m21_xml)
    tree = ET.ElementTree(root)
    for note_tag in root.findall('.//footnote/..'):
        footnote_tag = note_tag.find('footnote')
        note = Note.from_repr(footnote_tag.text)
        if any(note.eq_2d(n) for n in smrpy_notes):
            note_tag.attrib.update({'color': color})
            notehead_tag = ET.SubElement(note_tag, 'notehead', attrib={'color': color, 'parantheses': 'no'})
            notehead_tag.text = 'normal'
    output = io.StringIO()
    tree.write(output, encoding="unicode")
    return output.getvalue()

def generate_notes(symbolic_data):
    st = music21.converter.parse(base64.b64decode(symbolic_data))
    nps = indexers.NotePointSet(st)
    for n in nps:
        yield {
            'pid': -1,
            'n': Note.from_m21(n, -1).to_point()
        }
