from pathlib import Path
from typing import Dict, List
from uuid import uuid4

from excel_provider.io.excel import read_excel


class RestHandler:
    def __init__(self):
        self.data: Dict[str, Dict] = None
        self.sheets: Dict[str, str] = None

    def read_data(self, excel_file: Path, sheets: List[str], data_cols: List[str], index_cols: List[int] = None):
        self.data = read_excel(excel_file, sheets, data_cols, index_cols)
        self.sheets = {uuid4(): sheet for sheet in sheets}

    def get_data(self, sheet_id: str) -> Dict:
        if sheet := self.sheets.get(sheet_id):
            return self.data[sheet]
        else:
            raise ValueError(f"Sheet with id {sheet_id} does not exist")

    def get_sheet_names(self) -> Dict[str, str]:
        return self.sheets