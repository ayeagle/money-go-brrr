#!/bin/bash

set -e
source .env

curl -X GET "https://$PAPER_API_ENDPOINT/v2/account" \
    -H "APCA-API-KEY-ID: $PAPER_API_KEY_ID" \
    -H "APCA-API-SECRET-KEY: $PAPER_API_SECRET_KEY"
