from pathlib import Path
from typing import Dict, List
from uuid import uuid4

from excel_provider.io.excel import read_excel


class RestHandler:
    def __init__(self, handler_config: Dict = None):
        self.data: Dict[str, Dict] = None
        self.sheets: Dict[str, str] = None
        self.config = handler_config

    def read_data(self):
        if self.config is None:
            raise ValueError("Handler config is not set")

        if not self.config_valid():
            raise ValueError("Handler config is not valid")

        read_config = {
            "file": Path(self.config["excel_file"]),
            "sheets": self.config["sheets"],
            "data_cols": self.config["data_cols"],
            "index_cols": self.config.get("index_cols"),
        }

        self.data = read_excel(**read_config)
        self.sheets = [
            {"id": str(uuid4()), "name": sheet} for sheet in self.data.keys()
        ]

    def config_valid(self) -> bool:
        return (
            self.config is not None
            and self.config.get("excel_file") is not None
            and isinstance(self.config.get("sheets"), list)
            and isinstance(self.config.get("data_cols"), list)
        )

    def get_data(self, sheet_id: str) -> Dict:
        if self.sheets is None or self.data is None:
            raise ValueError("Data has not been read")

        if sheet := self._get_sheet_name_by_id(sheet_id):
            return {
                "id": sheet_id,
                "name": sheet,
                "series": [
                    {"name": name, "rows": rows}
                    for name, rows in self.data[sheet].items()
                ],
            }
        else:
            raise ValueError(f"Sheet with id {sheet_id} does not exist")

    def _get_sheet_name_by_id(self, sheet_id: str) -> str:
        for id, name in self.sheets.items():
            if id == sheet_id:
                return name
        return None

    def get_sheet_names(self) -> Dict[str, str]:
        if self.sheets is None:
            raise ValueError("Data has not been read")

        return {"sheets": self.sheets}
