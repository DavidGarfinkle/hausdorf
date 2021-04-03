CREATE TABLE IF NOT EXISTS Piece (
  pid SERIAL PRIMARY KEY,
  fmt TEXT,
  symbolic_data TEXT,
  music21_xml TEXT,
  composer TEXT,
  name TEXT,
  filename TEXT,
  collection_id INTEGER,
  window_size INTEGER
);

CREATE TABLE IF NOT EXISTS Note (
  n POINT,
  pid INTEGER REFERENCES Piece(pid),
  nid INTEGER,
  PRIMARY KEY (pid, nid)
);

CREATE TABLE IF NOT EXISTS MeasureOnsetMap (
  onset NUMERIC,
  mid INTEGER,
  pid INTEGER REFERENCES PIECE(pid),
  PRIMARY KEY (pid, mid, onset)
);

CREATE TABLE IF NOT EXISTS NoteWindow (
  pid INTEGER REFERENCES Piece(pid),
  onset_start NUMERIC,
  onset_end NUMERIC,
  u INTEGER, -- todo make this a single "scale" factor
  v INTEGER,
  unnormalized POINT[],
  normalized POINT[],
  PRIMARY KEY (pid, u, v, onset_start, onset_end)
);

--CREATE TABLE IF NOT EXISTS Posting (
--  id SERIAL PRIMARY KEY,
--  n POINT,
--  pid INTEGER,
--  u INTEGER,
--  v INTEGER,
--  nid INTEGER,
--  FOREIGN KEY (pid, nid) REFERENCES Note(pid, nid)
--  --FOREIGN KEY (pid, u, v) REFERENCES NormalizedWindow(pid, u, v)
--);
