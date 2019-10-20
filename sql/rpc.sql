CREATE EXTENSION plpython3u;

CREATE OR REPLACE FUNCTION index_piece() RETURNS TRIGGER AS $$
  from smrpy import index_piece
  index_piece(TD["new"]["pid"], TD["new"]["symbolic_data"])
$$ LANGUAGE plpython3u;

CREATE TRIGGER index_piece_after_insert AFTER INSERT ON Piece FOR EACH ROW EXECUTE PROCEDURE index_piece();

CREATE OR REPLACE FUNCTION search(query POINT[]) RETURNS TABLE(pid INTEGER, nids INTEGER[], notes POINT[]) AS $$
    from smrpy import search
    return search(query)
$$ LANGUAGE plpython3u IMMUTABLE STRICT;

--CREATE OR REPLACE FUNCTION normalize_window(window POINT[], u INTEGER, v INTEGER) RETURNS POINT[] AS $$
    

CREATE OR REPLACE FUNCTION search_sql(normalized_query POINT[]) RETURNS TABLE(pid INTEGER, nids INTEGER[], notes POINT[]) AS $$
    WITH
    pattern_notes AS (SELECT unnest(normalized_query) AS n),
    postings AS (
            SELECT Note.n, Note.pid, Note.nid, Posting.u, Posting.v
            FROM Posting JOIN Note ON Note.pid = Posting.pid AND Note.nid = Posting.nid
            JOIN pattern_notes ON Posting.n ~= pattern_notes.n
            ORDER BY (Note.pid, Posting.u, Posting.v, Note.nid) ASC),
    occs_by_window AS (
        SELECT DISTINCT ON (nids) postings.pid, array_agg(postings.nid) AS nids, array_agg(postings.n) AS notes, postings.u, postings.v
        FROM postings
        GROUP BY (postings.pid, postings.u, postings.v))
    SELECT occs_by_window.pid, occs_by_window.nids, occs_by_window.notes
    FROM occs_by_window;
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION excerpt(pid INTEGER, nids INTEGER[]) RETURNS TEXT AS $$
    from smrpy import excerpt
    return excerpt(pid, nids)
$$ LANGUAGE plpython3u IMMUTABLE STRICT;
