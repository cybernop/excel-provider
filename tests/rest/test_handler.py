import json
from datetime import date
from typing import Dict

from deepdiff import DeepDiff

from excel_provider.models import DataSeries
from excel_provider.provider import BaseProvider
from excel_provider.rest.handler import RestHandler

DATA = {
    "one": DataSeries(
        id="one",
        name="Sheet1",
        column="Value",
        rows={date(2024, 1, 1): 1, date(2024, 1, 2): 2},
    ),
    "two": DataSeries(
        id="two",
        name="Sheet2",
        column="Name",
        rows={1: "Jane", 2: "John"},
    ),
}


class DummyProvider(BaseProvider):
    def __init__(self, data: Dict[str, DataSeries]):
        self.data = data

    def get_series_names(self):
        return [{"id": id, "name": series.name} for id, series in self.data.items()]

    def get_series(self, series_id):
        return self.data.get(series_id)


def setup_handler(data):
    provider = DummyProvider(data)
    return RestHandler(provider)


def test_get_sheet_names():
    expected = {
        "sheets": [{"id": "one", "name": "Sheet1"}, {"id": "two", "name": "Sheet2"}]
    }
    handler = setup_handler(DATA)

    result = handler.get_sheet_names()
    assert DeepDiff(expected, result) == {}


def test_get_sheet_names_no_data():
    expected = {"sheets": []}
    handler = setup_handler(dict())

    result = handler.get_sheet_names()
    assert DeepDiff(expected, result) == {}


def test_get_data():
    handler = setup_handler(DATA)

    expected = [
        (
            "one",
            {
                "id": "one",
                "name": "Sheet1",
                "column": "Value",
                "rows": {"2024-01-01": 1, "2024-01-02": 2},
            },
        ),
        (
            "two",
            {
                "id": "two",
                "name": "Sheet2",
                "column": "Name",
                "rows": {"1": "Jane", "2": "John"},
            },
        ),
    ]

    for input, expected_entry in expected:
        result = handler.get_data(input)
        result = json.loads(result)
        assert DeepDiff(expected_entry, result) == {}


def test_get_data_not_existing():
    handler = setup_handler(DATA)

    result = handler.get_data("three")
    assert result is None


def test_get_data_no_data():
    handler = setup_handler(dict())

    result = handler.get_data("one")
    assert result is None
