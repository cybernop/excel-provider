import json
from datetime import date
from typing import Any, Dict


class DataSeries:
    def __init__(self, id: str, name: str, column: str, rows: Dict[Any, Any]):
        # Validate data types
        if not isinstance(id, str):
            raise TypeError("'id' is not of type 'str'")
        if not isinstance(name, str):
            raise TypeError("'name' is not of type 'str'")
        if not isinstance(column, str):
            raise TypeError("'column' is not of type 'str'")
        if not isinstance(rows, dict):
            raise TypeError("'rows' is not of type 'dict'")
        for key, value in rows.items():
            if isinstance(key, dict) or isinstance(value, dict):
                raise TypeError("no nesting allowed for 'rows'")

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
