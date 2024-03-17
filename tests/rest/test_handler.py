from excel_provider.rest.handler import RestHandler


def test_get_sheet_names():
    handler = RestHandler()
    handler.sheets = {"1": "Sheet1", "2": "Sheet2"}

    assert handler.get_sheet_names() == {"sheets": {"1": "Sheet1", "2": "Sheet2"}}


def test_get_sheet_names_no_data():
    handler = RestHandler()

    try:
        handler.get_sheet_names()
    except ValueError as e:
        assert str(e) == "Data has not been read"
    else:
        assert False


def test_get_data():
    handler = RestHandler()
    handler.data = {
        "Sheet1": {"Value": {1: 1, 2: 2}},
        "Sheet2": {"Name": {1: "Jane", 2: "John"}},
    }
    handler.sheets = [{"id": "1", "name": "Sheet1"}, {"id": "2", "name": "Sheet2"}]

    test_data = [
        (
            "1",
            {
                "id": "1",
                "name": "Sheet1",
                "series": [{"name": "Value", "rows": {1: 1, 2: 2}}],
            },
        ),
        (
            "2",
            {
                "id": "2",
                "name": "Sheet2",
                "series": [{"name": "Name", "rows": {1: "Jane", 2: "John"}}],
            },
        ),
    ]

    for input, expected in test_data:
        assert handler.get_data(input) == expected


def test_get_data_no_data():
    handler = RestHandler()
    handler.sheets = {"1": "Sheet1", "2": "Sheet2"}

    try:
        handler.get_data("1")
    except ValueError as e:
        assert str(e) == "Data has not been read"
    else:
        assert False


def test_get_data_no_sheets():
    handler = RestHandler()
    handler.data = {
        "Sheet1": {"Value": {1: 1, 2: 2}},
        "Sheet2": {"Name": {1: "Jane", 2: "John"}},
    }

    try:
        handler.get_data("1")
    except ValueError as e:
        assert str(e) == "Data has not been read"
    else:
        assert False


def test_get_data_sheet_not_found():
    handler = RestHandler()
    handler.data = {
        "Sheet1": {"Value": {1: 1, 2: 2}},
        "Sheet2": {"Name": {1: "Jane", 2: "John"}},
    }
    handler.sheets = [{"id": "1", "name": "Sheet1"}, {"id": "2", "name": "Sheet2"}]

    try:
        handler.get_data("3")
    except ValueError as e:
        assert str(e) == "Sheet with id 3 does not exist"
    else:
        assert False


def test_config_valid():
    handler = RestHandler(
        handler_config={
            "excel_file": "test.xlsx",
            "sheets": ["Sheet1", "Sheet2"],
            "data_cols": ["Value", "Name"],
        }
    )

    assert handler.config_valid() == True


def test_config_valid_no_config():
    handler = RestHandler()

    assert handler.config_valid() == False


def test_config_valid_no_excel_file():
    handler = RestHandler(
        handler_config={"sheets": ["Sheet1", "Sheet2"], "data_cols": ["Value", "Name"]}
    )

    assert handler.config_valid() == False


def test_config_valid_no_sheets():
    handler = RestHandler(
        handler_config={"excel_file": "test.xlsx", "data_cols": ["Value", "Name"]}
    )

    assert handler.config_valid() == False


def test_config_valid_sheets_no_list():
    handler = RestHandler(
        handler_config={
            "excel_file": "test.xlsx",
            "data_cols": ["Value", "Name"],
            "sheets": "Sheet1",
        }
    )

    assert handler.config_valid() == False


def test_config_valid_no_data_cols():
    handler = RestHandler(
        handler_config={"excel_file": "test.xlsx", "sheets": ["Sheet1", "Sheet2"]}
    )

    assert handler.config_valid() == False


def test_config_valid_data_cols_no_list():
    handler = RestHandler(
        handler_config={
            "excel_file": "test.xlsx",
            "sheets": ["Sheet1", "Sheet2"],
            "data_cols": "Value",
        }
    )

    assert handler.config_valid() == False
