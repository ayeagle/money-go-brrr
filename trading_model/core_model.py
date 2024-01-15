import random
from data.data_classes import DataProviderPayload

'''
Abstracted interface for ingesting the needed data
and returning buy/no buy decisions for SPY
'''


async def gen_run_core_model(data: DataProviderPayload) -> float:

    # this is where the magic happens
    # data payload needs to be the input
    # but return types can vary
    # right now loosely set up to represent
    # the num of fractional SPY shares to buy
    # where negative shares is a sell

    random_float = round(random.uniform(-5, 5), 2)

    return random_float
