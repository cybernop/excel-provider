import json
from datetime import date, datetime
from typing import Dict

from pandas import Timestamp


class DataSeries:
    def __init__(self, name: str, rows: Dict[datetime, int]):
        self.name = name
        self.rows = {
            (
                key.date()
                if isinstance(key, datetime) or isinstance(key, Timestamp)
                else key
            ): value
            for key, value in rows.items()
        }

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "rows": {
                k.isoformat() if isinstance(k, date) else str(k): v
                for k, v in self.rows.items()
            },
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            sort_keys=True,
        )
