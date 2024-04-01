from copy import deepcopy
from datetime import date

from deepdiff import DeepDiff

from excel_provider.error import ConfigMissingFieldError
from excel_provider.provider.excel_provider import ExcelProvider, ExcelProviderConfig

CONFIG = {
    "file": "tests/data/test.xlsx",
    "data": [
        {"id": "one", "sheet": "Sheet1", "data_col": "Value"},
        {"id": "two", "sheet": "Sheet2", "data_col": "Name"},
    ],
}


def test_excel_provider_initialize():
    provider = ExcelProvider(CONFIG)
    assert isinstance(provider.config, dict)

    provider.initialize()
    assert isinstance(provider.config, ExcelProviderConfig)

    assert list(provider.data.keys()) == ["one", "two"]

    assert provider.data["one"].name == "Sheet1"
    assert "Value" in provider.data["one"].rows
    assert len(provider.data["one"].rows["Value"]) == 3
    assert date(2024, 1, 1) in provider.data["one"].rows["Value"]
    assert provider.data["one"].rows["Value"][date(2024, 1, 1)] == 1

    assert "Name" in provider.data["two"].rows
    assert len(provider.data["two"].rows["Name"]) == 4
    assert 1 in provider.data["two"].rows["Name"]
    assert provider.data["two"].rows["Name"][1] == "Jane"


def test_excel_provider_get_series_names():
    expected = [{"id": "one", "name": "Sheet1"}, {"id": "two", "name": "Sheet2"}]

    provider = ExcelProvider(CONFIG)
    provider.initialize()

    result = provider.get_series_names()
    assert DeepDiff(expected, result) == {}


def test_excel_provider_get_series():
    expected = {
        "name": "Sheet1",
        "rows": {
            "Value": {date(2024, 1, 1): 1, date(2024, 1, 2): 2, date(2024, 1, 3): 3}
        },
    }

    provider = ExcelProvider(CONFIG)
    provider.initialize()

    result = provider.get_series("one")
    assert DeepDiff(expected, result.__dict__) == {}


def test_excel_provider_config():
    result = ExcelProviderConfig(CONFIG)

    assert result.file == "tests/data/test.xlsx"

    assert len(result.data) == 2
    assert result.data[0].id == "one"
    assert result.data[0].sheet == "Sheet1"
    assert result.data[0].data_col == "Value"


def test_excel_provider_config_missing_file():
    input = deepcopy(CONFIG)
    del input["file"]

    try:
        result = ExcelProviderConfig(input)
    except ConfigMissingFieldError as e:
        assert str(e) == "missing field 'file'"
    else:
        assert False


def test_excel_provider_config_missing_data():
    input = deepcopy(CONFIG)
    del input["data"]

    try:
        result = ExcelProviderConfig(input)
    except ConfigMissingFieldError as e:
        assert str(e) == "missing field 'data'"
    else:
        assert False


def test_excel_provider_config_missing_data_id():
    input = deepcopy(CONFIG)
    del input["data"][0]["id"]

    try:
        result = ExcelProviderConfig(input)
    except ConfigMissingFieldError as e:
        assert str(e) == "missing field 'data -> id'"
    else:
        assert False


def test_excel_provider_config_missing_data_sheet():
    input = deepcopy(CONFIG)
    del input["data"][0]["sheet"]

    try:
        result = ExcelProviderConfig(input)
    except ConfigMissingFieldError as e:
        assert str(e) == "missing field 'data -> sheet'"
    else:
        assert False


def test_excel_provider_config_missing_data_data_col():
    input = deepcopy(CONFIG)
    del input["data"][0]["data_col"]

    try:
        result = ExcelProviderConfig(input)
    except ConfigMissingFieldError as e:
        assert str(e) == "missing field 'data -> data_col'"
    else:
        assert False
