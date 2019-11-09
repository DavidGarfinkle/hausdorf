CREATE EXTENSION plpython3u;

CREATE OR REPLACE FUNCTION index_piece() RETURNS TRIGGER AS $$
  from smrpy import index_piece
  index_piece(TD["new"]["pid"], TD["new"]["symbolic_data"] or "")
$$ LANGUAGE plpython3u;

CREATE TRIGGER index_piece_after_insert AFTER INSERT OR UPDATE OF symbolic_Data ON Piece FOR EACH ROW EXECUTE PROCEDURE index_piece();

CREATE OR REPLACE FUNCTION search(query POINT[]) RETURNS TABLE(pid INTEGER, nids INTEGER[], notes POINT[]) AS $$
    from smrpy import search
    return search(query)
$$ LANGUAGE plpython3u IMMUTABLE STRICT;

--CREATE OR REPLACE FUNCTION normalize_window(window POINT[], u INTEGER, v INTEGER) RETURNS POINT[] AS $$
    

CREATE OR REPLACE FUNCTION search_sql(normalized_query POINT[]) RETURNS TABLE(pid INTEGER, notes POINT[]) AS $$
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
    SELECT occs_by_window.pid, occs_by_window.notes
    FROM occs_by_window;
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION excerpt(pid INTEGER, nids INTEGER[]) RETURNS TEXT AS $$
    from smrpy import excerpt
    return excerpt(pid, nids)
$$ LANGUAGE plpython3u IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION search_gin(normalized_query POINT[], threshold INTEGER) RETURNS TABLE(pid INTEGER, notes POINT[])
AS $$
    WITH matching_windows as (
                SELECT pid, u, v, normalized, unnormalized
                FROM notewindow
                WHERE (normalized && normalized_query)
        )
        ,pattern_notes AS (SELECT ARRAY[unnest(normalized_query)::POINT] AS n)                                           
        ,window_note_matches AS (
                SELECT w.pid, u, v,
                w.unnormalized[array_position(w.normalized, pattern_notes.n[1])] AS note                                 
                from pattern_notes join matching_windows AS W                                                            
                ON pattern_notes.n <@ w.normalized
        )
        SELECT pid, array_agg(note) notes                                          
        FROM window_note_matches
        GROUP BY (pid, u, v)
        HAVING count(*) > threshold
$$ LANGUAGE SQL;
