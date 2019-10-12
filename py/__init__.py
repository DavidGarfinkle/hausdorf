from smrpy.piece import Piece
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
    plpy.execute(plan, values)

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
