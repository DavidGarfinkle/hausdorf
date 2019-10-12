CREATE TABLE IF NOT EXISTS Piece (
  pid SERIAL PRIMARY KEY,
  fmt TEXT,
  data BYTEA,
  name TEXT,
  collection_id INTEGER
);

CREATE TABLE IF NOT EXISTS Note (
  n POINT,
  pid INTEGER REFERENCES Piece(pid),
  nid INTEGER,
  PRIMARY KEY (pid, nid)
);

CREATE TABLE IF NOT EXISTS NormalizedWindow (
  u INTEGER,
  v INTEGER,
  normalized POINT[],
  pid INTEGER REFERENCES Piece(pid),
  len INTEGER,
  FOREIGN KEY (pid, u) REFERENCES Note(pid, nid),
  FOREIGN KEY (pid, v) REFERENCES Note(pid, nid),
  PRIMARY KEY (pid, u, v)
);

CREATE TABLE IF NOT EXISTS Posting (
  id SERIAL PRIMARY KEY,
  n POINT,
  pid INTEGER,
  u INTEGER,
  v INTEGER,
  nid INTEGER,
  FOREIGN KEY (pid, nid) REFERENCES Note(pid, nid)
  --FOREIGN KEY (pid, u, v) REFERENCES NormalizedWindow(pid, u, v)
);
