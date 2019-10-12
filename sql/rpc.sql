CREATE EXTENSION plpython3u;

CREATE OR REPLACE FUNCTION index_piece() RETURNS TRIGGER AS $$
  from smrpy import index_piece
  index_piece(TD["new"]["pid"], TD["new"]["data"])
$$ LANGUAGE plpython3u;

CREATE TRIGGER index_piece_after_insert AFTER INSERT ON Piece FOR EACH ROW EXECUTE PROCEDURE index_piece();

CREATE OR REPLACE FUNCTION search(query JSONB) RETURNS TABLE(pid INTEGER, nids INTEGER[]) AS $$
    from smrpy import search
    return search(query)
$$ LANGUAGE plpython3u;
