from collections import namedtuple
from smrpy.piece import Piece, Note
from smrpy.hausdorf import generate_normalized_windows_with_notes

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

    for n in p.notes:
        plpy_execute(*(n.insert_str(pg_id)))

    for (u, v), normalized_window in generate_normalized_windows_with_notes(p.notes, 10):
        for i, n in enumerate(normalized_window[1:], 1):
            plpy_execute(posting_query, ("point", "integer", "integer", "integer", "integer"),
                ((n.onset, n.pitch), pg_id, u.index, v.index, n.index))

def notes_from_input(inp):
    import json
    point_array = json.loads(inp)
    return [Note(p['x'], None, p['y'], i) for i, p, in enumerate(point_array)]

PostingKey = namedtuple('PostingKey', ['pid', 'u', 'v'])

def search(query):
    notes = notes_from_input(query)
    m = []
    for (u, v), window in generate_normalized_windows_with_notes(notes, len(notes)):
        matches = {}
        for n in window:
            postings = plpy_execute("SELECT * FROM Posting WHERE n ~= %s", ("point",), ((n.onset, n.pitch),))
            for posting in postings:
                pid, u, v, j = posting["pid"], posting["u"], posting["v"], posting["nid"]
                key = PostingKey(pid, u, v)
                matches[key] = matches.get(key, ((u, 0),)) + ((j, n.index),)
        m.append(matches)
    res = set((key.pid, c[key]) for c in m for key in c if len(c[key]) == len(notes))
    pg_result = ([{"pid": k, "nids": [t[0] for t in v]} for k, v in res])
    return pg_result
