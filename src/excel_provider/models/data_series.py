import json
from datetime import date
from typing import Dict


class DataSeries:
    def __init__(self, name: str, rows: Dict[date, int]):
        self.name = name
        self.rows = rows

    def to_json(self) -> str:
        return json.dumps(
            {
                "name": self.name,
                "rows": {k.isoformat(): v for k, v in self.rows.items()},
            },
            sort_keys=True,
        )
