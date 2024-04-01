from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from excel_provider.error import ConfigMissingFieldError
from excel_provider.models import DataSeries

from .base_provider import BaseProvider


class ExcelProvider(BaseProvider):
    def __init__(self, config: dict = None):
        super().__init__(config)
        self.data: Dict[str, DataSeries] = {}

    def initialize(self):
        if isinstance(self.config, dict):
            self.config = ExcelProviderConfig(self.config)

        self._read_data()

    def _read_data(self):
        for data in self.config.data:
            df = pd.read_excel(
                self.config.file,
                sheet_name=data.sheet,
                engine="openpyxl",
                index_col=data.index_col,
                header=0,
                parse_dates=True,
            )

            sheet_result = df[[data.data_col]].dropna(subset=[data.data_col]).to_dict()

            # Convert the index to string to avoid issues with JSON serialization
            sheet_result = {
                _convert_key(k): v for k, v in sheet_result[data.data_col].items()
            }

            self.data[data.id] = DataSeries(
                id=data.id, name=data.sheet, column=data.data_col, rows=sheet_result
            )

    def get_series_names(self) -> List[Dict[str, str]]:
        return [{"id": id, "name": series.name} for id, series in self.data.items()]

    def get_series(self, series_id) -> DataSeries:
        return self.data.get(series_id)


def _convert_key(key) -> Any:
    if isinstance(key, int) or isinstance(key, float) or isinstance(key, bool):
        return key
    elif isinstance(key, datetime):
        return key.date()
    else:
        return str(key)


class ExcelProviderDataConfig:
    def __init__(self, config: dict = None) -> None:
        self.id: str = None
        self.sheet: str = None
        self.data_col: str = None
        self.index_col: int = None

        if config is not None:
            try:
                for entry in ["id", "sheet", "data_col"]:
                    setattr(self, entry, config[entry])
            except KeyError as e:
                raise ConfigMissingFieldError(e.args[0])

        self.index_col = config.get("index_col", 0)


class ExcelProviderConfig:
    def __init__(self, config: dict = None) -> None:
        self.file: str = None
        self.data: List[ExcelProviderDataConfig] = None

        if config is not None:
            try:
                self.file = config["file"]
                self.data = [ExcelProviderDataConfig(entry) for entry in config["data"]]
            except KeyError as e:
                raise ConfigMissingFieldError(e.args[0])
            except ConfigMissingFieldError as e:
                raise ConfigMissingFieldError("data", e)
