import sys
import os
import music21
import base64
import psycopg2.extensions
from smrpy import indexers
from smrpy import smr_pb2
from dataclasses import dataclass

def m21_score_to_xml_write(m21_score):
    o = m21_score.write('xml')
    with open(o, 'rb') as f:
        xml = f.read()
    os.remove(o)
    return xml

@dataclass
class Piece:
  data: str
  pid: int = None
  name: str = ""
  fmt: str = ""
  collection_id: int = 0

  def __post_init__(self):
    stream = music21.converter.parse(self.data)
    stream.makeNotation(inPlace=True)
    xml = m21_score_to_xml_write(stream)
    self.music21_xml = xml
    self.notes = [Note(n.offset, n.offset + n.duration.quarterLength, n.pitch.ps, i) for i, n in enumerate(indexers.NotePointSet(stream))]
  
  def insert_str(self):
    if self.pid: 
        vt = (
            (self.pid, "integer"),
            (self.fmt, "text"),
            (self.data, "text"),
            (base64.b64encode(self.music21_xml).decode('utf-8'), "text"),
            (self.name, "text"),
            (self.collection_id, "integer"))
        values, types = zip(*vt)
        return ("""
        INSERT INTO Piece (pid, fmt, symbolic_data, music21_xml, name, collection_id)
        VALUES(%s, %s, %s, %s, %s, %s)
        RETURNING pid;
        """, types, values)
    else:
        return ("""
        INSERT INTO Piece (fmt, data, name, collection_id)
        VALUES(%s, %s, %s, %s)
        RETURNING pid;
        """, types[1:], values[1:])

@dataclass
class Note:
    onset: float
    duration: int
    pitch: int
    index: int

    def __post_init__(self):
        self.onset = float(self.onset)
        self.pitch = int(self.pitch)
    
    def __hash__(self):
      return hash((self.onset, self.pitch))

    def insert_str(self, pid):
        return ("""
        INSERT INTO Note(n, pid, nid)
        VALUES (%s, %s, %s);
        """,
        ("point", "integer", "integer"),
        (self, pid, self.index))

    def getquoted(self):
        o = psycopg2.extensions.adapt(self.onset).getquoted()
        p = psycopg2.extensions.adapt(self.pitch).getquoted()
        return b"'(%s, %s)'" % (o, p)

    def __conform__(self, proto):
        if proto is psycopg2.extensions.ISQLQuote:
            return self

    def to_pb(self, piece_idx = None):
        return smr_pb2.Note(onset=self.onset, offset=None, pitch=int(self.pitch), piece_idx = piece_idx if piece_idx else self.index)

@dataclass
class NoteWindow:
    pid: int
    u: int
    v: int
    normalized: list
    unnormalized: list
