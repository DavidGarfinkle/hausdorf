import ast
import base64
import music21
import urllib.parse
from collections import namedtuple
from smrpy.indexers import NotePointSet
from smrpy.piece import Piece, Note
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
    posting_query = """
        INSERT INTO Posting (n, pid, u, v, nid)
        VALUES (%s, %s, %s, %s, %s)
    """
    p = Piece(data)
    plpy_execute("UPDATE Piece SET music21_xml=%s WHERE pid=%s", ("text", "integer"), (p.data, pg_id))

    for n in p.notes:
        plpy_execute(*(n.insert_str(pg_id)))

    for (u, v), normalized_window in generate_normalized_windows_with_notes(p.notes, 10):
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
    #stream = music21.converter.parse(query)
    #points = [(x.onset, x.pitch.ps) for x in NotePointSet(query)]
    notes = notes_from_points(query)
    m = []
    for (u, v), window in generate_normalized_windows_with_notes(notes, len(notes)):
        ps = [(n.onset, n.pitch) for n in window]
        query_string = "SELECT * FROM search_sql('{" + ",".join(f'"({x[0]},{x[1]})"' for x in ps) + "}')"
        results = plpy_execute(query_string, (), ())
        for r in results:
            if tuple(r['nids']) not in (tuple(x['nids']) for x in m):
                m.extend(results)
    return m

def excerpt(pid, nids):
    symbolic_data_query = "SELECT music21_xml FROM Piece WHERE pid=%s"
    symbolic_data, = plpy_execute(symbolic_data_query, ("integer",), (pid,))
    return coloured_excerpt(symbolic_data['music21_xml'], nids)

