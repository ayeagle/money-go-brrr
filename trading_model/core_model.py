
from data.data_classes import DataProviderPayload

'''
Abstracted interface for ingesting the needed data
and returning buy/no buy decisions for SPY
'''
async def gen_run_core_model(data: DataProviderPayload) -> int:

    ## this is where the magic happens
    ## data payload needs to be the input
    # but return types can vary

    return 0


