import json

from .data_series import DataSeries


class DataSerieses:
    def __init__(self, id: str, name: str, series: dict):
        self.id = id
        self.name = name
        self.series = [DataSeries(name, rows) for name, rows in series.items()]

    def to_json(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "name": self.name,
                "series": [series.to_dict() for series in self.series],
            },
            sort_keys=True,
        )
