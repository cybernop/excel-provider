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

        sheet_result = df[[data_col]].dropna(subset=[data_col]).to_dict()

        # Convert the index to string to avoid issues with JSON serialization
        sheet_result = {
            str(k): {_convert_key(vk): kk for vk, kk in v.items()}
            for k, v in sheet_result.items()
        }

        result[sheet] = sheet_result

    return result


def _convert_key(key) -> Any:
    if isinstance(key, int) or isinstance(key, float) or isinstance(key, bool):
        return key
    else:
        return str(key)
