CREATE EXTENSION plpython3u;

CREATE OR REPLACE FUNCTION index_piece() RETURNS TRIGGER AS $$
  from smrpy import index_piece
  index_piece(TD["new"]["pid"], TD["new"]["data"])
$$ LANGUAGE plpython3u;

CREATE TRIGGER index_piece_after_insert AFTER INSERT ON Piece FOR EACH ROW EXECUTE PROCEDURE index_piece();
