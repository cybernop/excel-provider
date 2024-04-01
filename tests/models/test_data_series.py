import json
from datetime import date

from excel_provider.models.data_series import DataSeries


def test_data_series_json():
    input = {
        "id": "test_id",
        "name": "test_series",
        "column": "test_column",
        "rows": {date(2024, 1, 1): 1, date(2024, 1, 2): 2},
    }
    expected = {
        "id": "test_id",
        "name": "test_series",
        "column": "test_column",
        "rows": {"2024-01-01": 1, "2024-01-02": 2},
    }

    series = DataSeries(**input)
    assert json.loads(series.to_json()) == expected
