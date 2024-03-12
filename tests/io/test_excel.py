from pandas import Timestamp

from excel_provider.io.excel import read_excel


def test_read_excel():
    result = read_excel(
        "tests/io/data/test.xlsx",
        sheets=["Sheet1", "Sheet2"],
        data_cols=["Value", "Name"],
    )

    assert len(result) == 2
    assert "Sheet1" in result
    assert "Sheet2" in result

    assert "Value" in result["Sheet1"]
    assert len(result["Sheet1"]["Value"]) == 3
    assert Timestamp("2024-01-01") in result["Sheet1"]["Value"]
    assert result["Sheet1"]["Value"][Timestamp("2024-01-01")] == 1

    assert "Name" in result["Sheet2"]
    assert len(result["Sheet2"]["Name"]) == 4
    assert 1 in result["Sheet2"]["Name"]
    assert result["Sheet2"]["Name"][1] == "Jane"
