CREATE EXTENSION plpython3u;

CREATE OR REPLACE FUNCTION index_piece() RETURNS TRIGGER AS $$
  from smrpy import index_piece
  index_piece(TD["new"]["pid"], TD["new"]["symbolic_data"])
$$ LANGUAGE plpython3u;

CREATE TRIGGER index_piece_after_insert AFTER INSERT ON Piece FOR EACH ROW EXECUTE PROCEDURE index_piece();

CREATE OR REPLACE FUNCTION search(p POINT[]) RETURNS TABLE(pid INTEGER, nids INTEGER[]) AS $$
    from smrpy import search
    return search(p)
$$ LANGUAGE plpython3u IMMUTABLE STRICT;

CREATE OR REPLACE FUNCTION excerpt(pid INTEGER, nids INTEGER[]) RETURNS TEXT AS $$
    from smrpy import excerpt
    return excerpt(pid, nids)
$$ LANGUAGE plpython3u IMMUTABLE STRICT;
