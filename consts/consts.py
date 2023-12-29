from enum import Enum


class WeatherCoords(Enum):
    NY_WALL_STREET = (40.70618619744728, -74.00914109658291)

class RunTypeParam(Enum):
    TEST = 'test'
    FULL_TEST = 'full_test'
    PROD = 'prod'
    PROD_DANGEROUS = 'prod_dangerous'
    DOWNLOAD = 'download'