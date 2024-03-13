from excel_provider.rest.handler import RestHandler


def test_get_sheet_names():
    handler = RestHandler()
    handler.sheets = {"1": "Sheet1", "2": "Sheet2"}

    assert handler.get_sheet_names() == {"1": "Sheet1", "2": "Sheet2"}

def test_get_data():
    handler = RestHandler()
    handler.data = {"Sheet1": {"Value": {1: 1, 2: 2}}, "Sheet2": {"Name": {1: "Jane", 2: "John"}}}
    handler.sheets = {"1": "Sheet1", "2": "Sheet2"}

    assert handler.get_data("1") == {"Value": {1: 1, 2: 2}}
    assert handler.get_data("2") == {"Name": {1: "Jane", 2: "John"}}

def test_get_data_sheet_not_found():
    handler = RestHandler()
    handler.sheets = {"1": "Sheet1", "2": "Sheet2"}

    try:
        handler.get_data("3")
    except ValueError as e:
        assert str(e) == "Sheet with id 3 does not exist"
    else:
        assert False