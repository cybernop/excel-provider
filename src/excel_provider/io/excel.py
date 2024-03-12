from pathlib import Path
from typing import Any, Dict, List

import pandas


def read_excel(
    file: Path, sheets: List[str], data_cols: List[str], index_cols: List[int] = None
) -> Dict[str, Dict[str, Any]]:
    result = {}

    if index_cols is None:
        index_cols = [0] * len(sheets)

    for sheet, data_col, index_col in zip(sheets, data_cols, index_cols):
        df = pandas.read_excel(
            file,
            sheet_name=sheet,
            engine="openpyxl",
            index_col=index_col,
            header=0,
            parse_dates=True,
        )

        result[sheet] = df[[data_col]].dropna(subset=[data_col]).to_dict()

    return result
