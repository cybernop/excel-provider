from typing import Dict

from excel_provider.provider import BaseProvider


class RestHandler:
    def __init__(self, provider: BaseProvider):
        self.provider = provider

    def get_data(self, sheet_id: str) -> Dict:
        result = self.provider.get_series(sheet_id)
        return result.to_json() if result is not None else None

    def get_sheet_names(self) -> Dict[str, str]:
        return {"sheets": self.provider.get_series_names()}
