#!/bin/bash

# Define the content of the .env file
ENV_CONTENT=$(cat <<EOF
API_ENDPOINT='api.alpaca.markets'
API_KEY_ID='mock_api_key_id'
API_SECRET_KEY='mock_api_secret_key'

PAPER_API_ENDPOINT='paper-api.alpaca.markets'
PAPER_API_KEY_ID='mock_paper_api_key_id'
PAPER_API_SECRET_KEY='mock_paper_api_secret_key'

READY_TO_TRADE='False'
EOF
)

# Create the .env file with the defined content
echo "$ENV_CONTENT" > .env.local

# Print a message indicating that the .env file has been created
echo "Mock .env file created."

