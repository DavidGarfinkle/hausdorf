#!/bin/bash

xk() {
    echo $1
    exit 1
}

PIECE_FILE=$2
METADATA_TYPE=$1
PIECE=$(basename ${PIECE_FILE})
if [[ -z "${PIECE}" ]]; then
    xk "Usage: insert_hausdorf.sh <piece>"
fi

python3 smrpy/metadata.py -t $METADATA_TYPE $PIECE_FILE > tmp
PIECE_ID=$(jq < tmp .pid -r )
PIECE_FORMAT=$(jq < tmp .fmt -r)
PIECE_COLLECTION_ID=$(jq < tmp .collection_id -r)
PIECE_NAME=$(jq < tmp .name -r)
PIECE_COMPOSER=$(jq < tmp .composer -r)

psql -c "INSERT INTO Piece(pid, name, fmt, collection_id, composer, filename) VALUES(${PIECE_ID}, '${PIECE_NAME}', '${PIECE_FORMAT}', ${PIECE_COLLECTION_ID}, '${PIECE_COMPOSER}', '${PIECE_FILE}')"
#base64 --wrap=0 < ${PIECE_FILE} | echo "'"$(cat -)"'" | psql -f - -c "COPY Piece (symbolic_data) FROM STDIN WHERE pid=${PIECE_ID}"
