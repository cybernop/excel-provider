from typing import Dict

from excel_provider.models import DataSeries


class BaseProvider:
    def __init__(self, config: dict = None):
        self.config = config

    def initialize(self):
        raise NotImplementedError()

    def get_series_names(self) -> Dict[str, str]:
        raise NotImplementedError()

    def get_series(self, series_id) -> DataSeries:
        raise NotImplementedError()
