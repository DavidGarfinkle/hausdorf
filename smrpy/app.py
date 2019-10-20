#!/usr/local/bin/python3
import os
from flask import Flask, request, jsonify, Response, send_from_directory, render_template
from smrpy.occurrence import filter_occurrences, OccurrenceFilters
from smrpy import occurrence, piece
from smrpy import indexers
import requests
import json

from response import build_response

application = Flask(__name__)
logger = application.logger

POSTGREST_URI = "http://localhost:3000/"

@application.route("/", methods=["GET"])
def index():
    return render_template("search.html", searchResponse = {})

@application.route("/dist/<path>", methods=["GET"])
def get_dist(path):
    return send_from_directory('templates', path)

@application.route("/index", methods=["POST"])
def index_no_oarg():
    return index(None)

def apiSearch(note_tuples):
    #p=\{\"(0,60)\",\"(0,64)\",\"(0,69)\",\"(0,72)\",\"(1,58)\",\"(1,65)\",\"(1,70)\",\"(1,74)\"\}"
    query_param = "{" + ",".join(f'"{tup}"' for up in note_tuples) + "}"
    return requests.get("localhost:3000/search", p = query_param)

def qstring(ps):
    return "{" + ','.join(f'\"({x[0]},{x[1]})\"' for x in ps) + "}"

@application.route("/excerpt", methods=["GET"])
def excerpt():
    piece_id = int(request.args.get("pid"))
    notes = [str(x) for x in request.args.get("nid").split(",")]
    excerpt_xml = requests.get("http://localhost:3000/rpc/excerpt", {"pid": piece_id, "nids": '{' + ','.join(notes) + '}'}).content
    return Response(excerpt_xml, mimetype='text/xml')

@application.route("/search", methods=["GET"])
def search():

    for arg in ("page", "rpp", "query", "tnps", "intervening", "inexact", "collection"):
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
    except ValueError as e:
        return Response(f"Failed to parse parameter(s) to integer, got exception {str(e)}", status=400)

    query_str = request.args.get("query")
    query_stream = indexers.parse(query_str)
    query_nps = indexers.NotePointSet(query_stream)
    query_notes = [(n.offset, n.pitch.ps) for n in query_nps]
    query_pb_notes = [piece.Note(n[0], None, n[1], i).to_pb() for i, n in enumerate(query_notes)]
    #resp = requests.get(POSTGREST_URI + "rpc/search", { "p": qstring(query_points) }).json()
    resp = requests.get("http://localhost:3000/rpc/search", params='query={\"(0.0,60.0)\",\"(0.0,64.0)\",\"(0.0,69.0)\",\"(0.0,72.0)\",\"(1.0,58.0)\",\"(1.0,65.0)\",\"(1.0,70.0)\",\"(1.0,74.0)\"}').json()
    occurrences = [occurrence.occ_to_occpb(occ) for occ in resp]

    occfilters = OccurrenceFilters(
            transpositions = range(*tnps_ints),
            intervening = intervening_ints,
            inexact = inexact_ints)

    search_response = build_response(
            filter_occurrences(occurrences, query_pb_notes, occfilters),
            rpp,
            page,
            tnps,
            intervening,
            query_str,
            inexact)

    if request.content_type == "application/json":
        return jsonify(search_response)
    else:
        return render_template("search.html", searchResponse = search_response)

def main():
    application.run(host="0.0.0.0", port=int(os.getenv('FLASK_PORT', 80)))

if __name__ == '__main__':
    main()
