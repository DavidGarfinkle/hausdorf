#!/bin/bash

xk() {
    echo $1
    exit 1
}

PIECE_FILE=$1
PIECE=$(basename $1)
if [[ -z "${PIECE}" ]]; then
    xk "Usage: insert_hausdorf.sh <piece>"
fi

PIECE_ID=$(cut -d '_' -f 1 <<< ${PIECE})
PIECE_NAME=$(cut -d '_' -f 2 <<< ${PIECE})
PIECE_COMPOSER=$(cut -d '_' -f 3 <<< ${PIECE})
PIECE_FORMAT=$(cut -d '.' -f 2 <<< ${PIECE})
PIECE_COLLECTION_ID=0
base64 --wrap=0 < ${PIECE_FILE} | xargs -I {} psql -c "INSERT INTO Piece(pid, name, fmt, collection_id, symbolic_data) VALUES(${PIECE_ID}, '${PIECE_NAME}', '${PIECE_FORMAT}', ${PIECE_COLLECTION_ID}, '{}')"
