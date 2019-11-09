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

PIECE_NUM_FIELDS=$(echo ${PIECE} | awk -F_ '{print NF}')
PIECE_ID=$(cut -d '_' -f 1 <<< ${PIECE})
PIECE_NAME=$(cut -d '_' -f 2-$(expr ${PIECE_NUM_FIELDS} - 2) <<< ${PIECE} | tr '-' ' ')
PIECE_COMPOSER=$(awk -F_ '{print $(NF-1)}' <<< ${PIECE} | tr '-' ' ')
PIECE_FORMAT=$(echo ${PIECE} | awk -F. '{print $NF}')
PIECE_COLLECTION_ID=0

echo -n ${PIECE_ID}, > tmp
echo -n ${PIECE_FORMAT}, >> tmp
base64 --wrap=0 < ${PIECE_FILE} >> tmp; echo -n "," >> tmp
echo -n '""', >> tmp
echo -n ${PIECE_COMPOSER}, >> tmp
echo -n ${PIECE_NAME}, >> tmp
echo -n ${PIECE_COLLECTION_ID} >> tmp

psql -c "INSERT INTO Piece(pid, name, fmt, collection_id, composer) VALUES(${PIECE_ID}, '${PIECE_NAME}', '${PIECE_FORMAT}', ${PIECE_COLLECTION_ID}, '${PIECE_COMPOSER}')"
#base64 --wrap=0 < ${PIECE_FILE} | echo "'"$(cat -)"'" | psql -f - -c "COPY Piece (symbolic_data) FROM STDIN WHERE pid=${PIECE_ID}"
