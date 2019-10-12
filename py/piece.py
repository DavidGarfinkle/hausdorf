import sys
import music21
import base64
from smrpy import indexers
from io import StringIO
from dataclasses import dataclass

def stream_to_xml(stream):
  sx = music21.musicxml.m21ToXml.ScoreExporter(stream)
  musicxml = sx.parse()
  bfr = StringIO()
  sys.stdout = bfr
  sx.dump(musicxml)
  output = bfr.getvalue()
  sys.stdout = sys.__stdout__
  return output

@dataclass
class Piece:
  data: bytes
  name: str = ""
  fmt: str = ""
  collection_id: int = 0

  def __post_init__(self):
    stream = music21.converter.parse(base64.b64decode(self.data))
    xml = stream_to_xml(stream)
    self.data = bytes(xml, encoding="utf-8")
    self.notes = [Note(n.offset, n.offset + n.duration.quarterLength, n.pitch.ps, i) for i, n in enumerate(indexers.NotePointSet(stream))]
  
  def insert_str(self):
    return ("""
    INSERT INTO Piece (fmt, data, name, collection_id)
    VALUES(%s, %s, %s, %s)
    RETURNING pid;
    """,
    ("text", "bytea", "text", "integer"),
    (self.fmt, self.data, self.name, self.collection_id))

  def update_str(self, pg_id):
    return ("""
    UPDATE Piece SET data=%s WHERE pid=%s
    """,
    ("bytea", "integer"),
    (self.data, pg_id))

@dataclass
class Note:
    onset: int
    duration: int
    pitch: int
    index: int
    
    def __hash__(self):
      return hash((self.onset, self.pitch))

    def insert_str(self, pid):
        return ("""
        INSERT INTO Note(n, pid, nid)
        VALUES (%s, %s, %s);
        """,
        ("point", "integer", "integer"),
        ((self.onset, self.pitch), pid, self.index))
