import os
from core_script.cli_formatters import formatWarningMessage
from consts.cli_messages import env_created_message
from consts.consts import KEYS_ENV_LOCATION

env_content = """
API_ENDPOINT='api.alpaca.markets'
API_KEY_ID='mock_api_key_id'
API_SECRET_KEY='mock_api_secret_key'

PAPER_API_ENDPOINT='paper-api.alpaca.markets'
PAPER_API_KEY_ID='mock_paper_api_key_id'
PAPER_API_SECRET_KEY='mock_paper_api_secret_key'

READY_TO_TRADE='False'
"""


if (os.path.exists(KEYS_ENV_LOCATION)):
    print("Env already exists.")
else:
    with open('.env', 'w') as env_file:
        env_file.write(env_content)
formatWarningMessage(env_created_message)
