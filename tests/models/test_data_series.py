import json
from datetime import date

from excel_provider.models.data_series import DataSeries


def test_data_series_json():
    input = {
        "name": "test_series",
        "rows": {date(2024, 1, 1): 1, date(2024, 1, 2): 2},
    }
    expected = {
        "name": "test_series",
        "rows": {"2024-01-01": 1, "2024-01-02": 2},
    }

    series = DataSeries(**input)
    assert json.loads(series.to_json()) == expected
