import itertools
import ntpath
import sys
import time
import threading


def get_global_data_dict(lovamap_data: dict) -> dict:
    return {
        str: [data['global']['values'][id]] for id, str in data['global']['names'].items()
    }

def get_intersubunit_data_dict(lovamap_data: dict) -> dict:
    result = {}
    for id, str in lovamap_data['intersubs']['names'].items():
        vals = lovamap_data['intersubs']['values'][id]
        if isinstance(vals, matlab.double):
            # Need to "flatten" the list because every element comes wrapped in its own list.
            result[str] = [val for sublist in vals for val in sublist]
        else:
            result[str] = vals
    return result

def get_subunit_data_dict(lovamap_data: dict) -> dict:
    result = {}
    for id, str in lovamap_data['subs']['names'].items():
        vals = lovamap_data['subs']['values'][id]
        if isinstance(vals, matlab.double):
            # Need to "flatten" the list because every element comes wrapped in its own list.
            result[str] = [val for sublist in vals for val in sublist]
        else:
            result[str] = vals
    return result

def data_dict_to_df(data_dict: dict) -> pd.DataFrame:
    # We don't expect all the data to be the same length, so we must concatenate ourselves.
    return pd.concat([pd.DataFrame({key: value}) for key, value in data_dict.items()], axis=1)

## Cell
import pandas as pd

# Form all three distinct DataFrames before gluing together to write to Excel.

df_global = data_dict_to_df(get_global_data_dict(lovamap_data))
df_intersubs = data_dict_to_df(get_intersubunit_data_dict(lovamap_data))
df_subs = data_dict_to_df(get_subunit_data_dict(lovamap_data))


## Cell
from pandas.io.formats import excel
excel.ExcelFormatter.header_style = None

# Take everything after the first underscore, but remove the extension.
# Only take at most 30 characters.
# sheet_name = replicate.split('_', 1)[1].split('.', 1)[0]
# sheet_name = sheet_name[:30] if len(sheet_name) > 30 else sheet_name

# with pd.ExcelWriter('./output.xlsx') as writer:
#     df_global.to_excel(writer, sheet_name=sheet_name, header=False, index=False, startrow=0, startcol=0)
#     df_intersubs.to_excel(writer, sheet_name=sheet_name, index=False, startrow=len(df_global.index), startcol=0)
#     df_subs.to_excel(writer, sheet_name=sheet_name, index=False, startrow=len(df_global.index), startcol=len(df_intersubs.columns))

# or do the following:

with pd.ExcelWriter('./output.xlsx') as writer:
    df_global.to_excel(writer, sheet_name='Global', index=False)
    df_intersubs.to_excel(writer, sheet_name='Intersub', index=False)
    df_subs.to_excel(writer, sheet_name='Subunit', index=False)
