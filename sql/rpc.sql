CREATE EXTENSION plpython3u;

CREATE OR REPLACE FUNCTION smrpy_index_piece() RETURNS TRIGGER AS $$
  from smrpy import index_piece
  index_piece(TD["new"]["pid"], TD["new"]["symbolic_data"] or "")
$$ LANGUAGE plpython3u;

CREATE OR REPLACE FUNCTION index_piece() RETURNS TRIGGER AS $$
BEGIN
    NEW.music21_xml = symbolic_data_to_m21_xml(NEW.symbolic_data);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER index_piece_after_insert BEFORE INSERT OR UPDATE OF symbolic_data ON Piece FOR EACH ROW EXECUTE PROCEDURE index_piece();

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
            JOIN pattern_notes ON Posting.n ~= pattern_notes.n),
    occs_by_window AS (
        SELECT postings.pid, array_agg(postings.n) AS notes, postings.u, postings.v
        FROM postings
        GROUP BY (postings.pid, postings.u, postings.v))
    SELECT occs_by_window.pid, occs_by_window.notes
    FROM occs_by_window;
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION search_sql_gin_exact(normalized_query POINT[]) RETURNS TABLE(pid INTEGER, notes POINT[]) AS
$$
WITH matching_windows AS (
        SELECT pid, u, v, normalized, unnormalized
        FROM notewindow
        WHERE (normalized @> normalized_query)),
    window_note_matches AS (
        SELECT w.pid, u, v, w.unnormalized[array_position(w.normalized, pattern_notes.n)] AS note
        FROM (SELECT unnest(normalized_query) AS n) AS pattern_notes JOIN matching_windows AS w
        ON true)
SELECT window_note_matches.pid, array_agg(note) notes
FROM window_note_matches
GROUP BY (window_note_matches.pid, u, v);
$$ LANGUAGE SQL;
	
CREATE OR REPLACE VIEW test_palestrina_search AS SELECT * FROM search_sql_gin_exact('{"(0.0, 0.0)","(0.0,4.0)","(0.0,9.0)","(0.0,12.0)","(1.0,-2.0)","(1.0,5.0)","(1.0,10.0)","(1.0,14.0)"}');

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

CREATE OR REPLACE FUNCTION generate_notewindows(notes POINT[], window_size INTEGER) RETURNS TABLE(like NoteWindow2) AS $$
    from smrpy import generate_notewindows
    return generate_notewindows(notes, window_size)
$$ LANGUAGE plpython3u IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION symbolic_data_to_m21_xml(symbolic_data TEXT) RETURNS TEXT AS $$
    from smrpy import symbolic_data_to_m21_xml
    return symbolic_data_to_m21_xml(symbolic_data)
$$ LANGUAGE plpython3u IMMUTABLE STRICT;
