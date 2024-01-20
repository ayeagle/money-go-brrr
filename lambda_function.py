from script_controller import main

"""
**********************************************************
AWS Lambda entry point
**********************************************************
"""

def lambda_handler(event, context):
    arg_value = event["arg"]
    main(arg_value)