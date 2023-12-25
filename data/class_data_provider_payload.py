from data.class_data_provider_params import DataProviderParams
from typing import Union
import pandas as pd


class DataProviderPayload:
    def __init__(
            self,
            params: DataProviderParams,
            diff_data_sources: dict,
            combined_data_sources: Union[dict, pd.DataFrame, str]
    ):
        self._params = params
        self._diff_data_sources = diff_data_sources
        self._combined_data_sources = combined_data_sources
        

    @property
    def params(self):
        return self._params
    
    @property
    def diff_data_sources(self):
        return self._diff_data_sources
    
    @property
    def combined_data_sources(self):
        return self._combined_data_sources
