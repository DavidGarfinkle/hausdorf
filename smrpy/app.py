#!/usr/local/bin/python3
import os
from flask import Flask, request, jsonify, Response, send_from_directory, render_template
from smrpy.occurrence import filter_occurrences, OccurrenceFilters
from smrpy import occurrence, piece
from smrpy import indexers
import requests
import json
from dataclasses import fields

import psycopg2
import time

from smrpy.response import build_response, QueryArgs
from smrpy.excerpt import coloured_excerpt

application = Flask(__name__)
logger = application.logger

POSTGREST_URI = os.environ.get("POSTGREST_URI", "http://localhost:3000")

def connect_to_psql():
    db_str = ' '.join(('='.join((k, os.environ[v])) if v in os.environ else "") for k, v in (
                ('host', 'PGHOST'),
                ('port', 'PGPORT'),
                ('dbname', 'PGDATABASE'),
                ('user', 'PGUSER'),
                ('password', 'PG_PASS'))) # TODO fix this line to match (and not go to stdout)?
    print("connecting to " + db_str)

    while True:
        try:
            conn = psycopg2.connect(db_str)
            break
        except Exception as e:
            time_to_wait = 5
            print(f"failed; waiting {time_to_wait} seconds...")
            time.sleep(time_to_wait)
            connect_to_psql()
    conn.autocommit = False

    application.config['PSQL_CONN'] = conn
    return conn

@application.route("/", methods=["GET"])
def index():
    return render_template("search.html", searchResponse = {})

@application.route("/dist/<path>", methods=["GET"])
def get_dist(path):
    return send_from_directory('templates', path)

@application.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory('templates', 'favicon.ico')

@application.route("/index", methods=["POST"])
def index_no_oarg():
    return index(None)

def qstring(ps):
    return "{" + ','.join(f'\"({x.onset},{x.pitch})\"' for x in ps) + "}"

@application.route("/excerpt", methods=["GET"])
def excerpt():
    db_conn = connect_to_psql()
    piece_id = int(request.args.get("pid"))
    notes = [str(x) for x in request.args.get("nid").split(",")]
    excerpt_xml = coloured_excerpt(db_conn, notes, piece_id)
    #excerpt_xml = requests.get("http://localhost:3000/rpc/excerpt", {"pid": piece_id, "nids": '{' + ','.join(notes) + '}'}).content
    return Response(excerpt_xml, mimetype='text/xml')

@application.route("/search", methods=["GET"])
def search():
    db_conn = connect_to_psql()

    for arg in (x.name for x in fields(QueryArgs)):
        missing = []
        if not request.args.get(arg):
            missing.append(arg)
        if missing:
            return Response(f"Missing GET parameter(s): {missing}", status=400)

    try:
        page = int(request.args.get("page"))
        rpp = int(request.args.get("rpp"))
        tnps = request.args.get("tnps").split(",")
        tnps_ints = list(map(int, tnps))
        tnps_ints[1] += 1 # increase range to include end
        intervening = request.args.get("intervening").split(",")
        intervening_ints = tuple(map(int, intervening))
        inexact = request.args.get("inexact").split(",")
        inexact_ints = tuple(map(int, inexact))
        collection = int(request.args.get("collection"))
        query_str = request.args.get("query")
        qargs = QueryArgs(rpp, page, tnps, intervening, inexact, collection, query_str)
    except ValueError as e:
        return Response(f"Failed to parse parameter(s) to integer, got exception {str(e)}", status=400)

    query_str = request.args.get("query")
    query_stream = indexers.parse(query_str)
    query_nps = indexers.NotePointSet(query_stream)
    query_notes = [(n.offset, n.pitch.ps) for n in query_nps]
    query_pb_notes = [piece.Note(n[0], None, n[1], i).to_pb() for i, n in enumerate(query_notes)]
    resp = requests.get(POSTGREST_URI + "/rpc/search", params=('query=' + qstring(query_pb_notes))).json()
    occurrences = [occurrence.occ_to_occpb(occ) for occ in resp]

    occfilters = OccurrenceFilters(
            transpositions = range(*tnps_ints),
            intervening = intervening_ints,
            inexact = inexact_ints)

    search_response = build_response(
            db_conn,
            filter_occurrences(occurrences, query_pb_notes, occfilters),
            qargs)

    if request.content_type == "application/json":
        return jsonify(search_response)
    else:
        return render_template("search.html", searchResponse = search_response)

def main():
    application.run(host="0.0.0.0", port=int(os.getenv('FLASK_PORT', 80)))

if __name__ == '__main__':
    main()
