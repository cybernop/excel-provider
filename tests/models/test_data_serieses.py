import json
from datetime import date

from deepdiff import DeepDiff

from excel_provider.models.data_serieses import DataSerieses


def test_data_serieses_json():
    input = {
        "id": "test_id",
        "name": "test_name",
        "series": {
            "test_series": {date(2024, 1, 1): 1, date(2024, 1, 2): 2},
        },
    }
    expected = {
        "id": "test_id",
        "name": "test_name",
        "series": [
            {
                "name": "test_series",
                "rows": {"2024-01-01": 1, "2024-01-02": 2},
            }
        ],
    }

    serieses = DataSerieses(**input)
    assert DeepDiff(json.loads(serieses.to_json()), expected) == {}
