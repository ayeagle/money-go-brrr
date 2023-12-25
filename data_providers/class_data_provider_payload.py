from data_providers.class_data_provider_params import DataProviderParams
from typing import Union
import pandas as pd


class DataProviderPayload:
    def __init__(
            self,
            params: DataProviderParams,
            diff_data_sources: dict,
            combined_data_sources: Union[dict, pd.DataFrame, str]
    ):
        self.params = params
        self.diff_data_sources = diff_data_sources
        self.combined_data_sources = combined_data_sources
        

    @property
    def params(self):
        return self.params
    
    @property
    def diff_data_sources(self):
        return self.diff_data_sources
    
    @property
    def combined_data_sources(self):
        return self.combined_data_sources
