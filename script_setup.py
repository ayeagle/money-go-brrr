from consts.cli_messages import env_created_message


env_content = """\
API_ENDPOINT='api.alpaca.markets'
API_KEY_ID='mock_api_key_id'
API_SECRET_KEY='mock_api_secret_key'

PAPER_API_ENDPOINT='paper-api.alpaca.markets'
PAPER_API_KEY_ID='mock_paper_api_key_id'
PAPER_API_SECRET_KEY='mock_paper_api_secret_key'

READY_TO_TRADE='False'
"""

with open('.env.local', 'w') as env_file:
    env_file.write(env_content)

print(env_created_message)
