import json
from datetime import date
from typing import Any, Dict


class DataSeries:
    def __init__(self, id: str, name: str, column: str, rows: Dict[Any, Any]):
        self.id = id
        self.name = name
        self.column = column
        self.rows = rows

    def to_json(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "name": self.name,
                "column": self.column,
                "rows": {
                    k.isoformat() if isinstance(k, date) else k: v
                    for k, v in self.rows.items()
                },
            },
            sort_keys=True,
        )
