import sys
import os
import music21
import base64
from smrpy import indexers
from smrpy import smr_pb2
from dataclasses import dataclass

def m21_score_to_xml_write(m21_score):
    o = m21_score.write('xml')
    with open(o, 'r') as f:
        xml = f.read()
    os.remove(o)
    return xml

@dataclass
class Piece:
  data: str
  name: str = ""
  fmt: str = ""
  collection_id: int = 0

  def __post_init__(self):
    stream = music21.converter.parse(base64.b64decode(self.data))
    stream.makeNotation(inPlace=True)
    xml = m21_score_to_xml_write(stream)
    self.data = xml
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
    onset: float
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

    def to_pb(self):
        return smr_pb2.Note(onset=self.onset, offset=None, pitch=int(self.pitch), piece_idx=self.index)
