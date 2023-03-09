import itertools
import sys
import time
import threading


ids = list(result['global']['names'])
global_dict = {
    'names': [result['global']['names'][id] for id in ids],
    'values': [result['global']['values'][id] for id in ids],
}

intersubs_dict = {}
for id, str in result['intersubs']['names'].items():
    vals = result['intersubs']['values'][id]
    if isinstance(vals, matlab.double):
        # Need to "flatten" the list because every element comes wrapped in its own list.
        intersubs_dict[str] = [val for sublist in vals for val in sublist]
    else:
        intersubs_dict[str] = vals

subs_dict = {}
for id, str in result['subs']['names'].items():
    vals = result['subs']['values'][id]
    if isinstance(vals, matlab.double):
        # Need to "flatten" the list because every element comes wrapped in its own list.
        subs_dict[str] = [val for sublist in vals for val in sublist]
    else:
        subs_dict[str] = vals

if isinstance(result['isInteriorSub'], matlab.logical):
    result['isInteriorSub'] = [val for sublist in result['isInteriorSub'] for val in sublist]



## Cell
import pandas as pd

# Form all three distinct DataFrames before gluing together to write to Excel.

df_global = pd.DataFrame.from_dict(global_dict)

df_intersubs = pd.DataFrame()
for key, value in intersubs_dict.items():
    df_intersubs = pd.concat([df_intersubs, pd.DataFrame({key: value})], axis=1)

df_subs = pd.DataFrame()
for key, value in subs_dict.items():
    df_subs = pd.concat([df_subs, pd.DataFrame({key: value})], axis=1)



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
    df_global.to_excel(writer, sheet_name='Global', header=False, index=False)
    df_intersubs.to_excel(writer, sheet_name='Intersub', index=False)
    df_subs.to_excel(writer, sheet_name='Subunit', index=False)


# Given a list of excel files, merge them into one file.
import ntpath
ntpath.basename("a/b/c")

all_dfs = {}
for file in excel_files:
    excel = pd.ExcelFile(file)
    all_dfs[file] = {sheet: excel.parse(sheet) for sheet in excel.sheet_names}

with pd.ExcelWriter('./output.xlsx') as writer:
    for file, dfs in all_dfs.items():
        # Take everything after the first underscore, but remove the extension.
        # Only take at most 30 characters.
        sheet_name = ntpath.basename(file).split('_', 1)[1].split('.', 1)[0]
        sheet_name = sheet_name[:30] if len(sheet_name) > 30 else sheet_name
        dfs['Global'].to_excel(writer, sheet_name=sheet_name, header=False, index=False, startrow=0, startcol=0)
        dfs['Intersub'].to_excel(writer, sheet_name=sheet_name, index=False, startrow=len(dfs['Global'].index), startcol=0)
        dfs['Subunit'].to_excel(writer, sheet_name=sheet_name, index=False, startrow=len(dfs['Global'].index), startcol=len(dfs['Intersub'].columns))

    # Write one final sheet of cumulated data
    df_all_global = pd.concat([dfs['Global'] for dfs in all_dfs.values()], axis=1)
    df_all_intersub = pd.concat([dfs['Intersub'] for dfs in all_dfs.values()], axis=0)
    df_all_sub = pd.concat([dfs['Subunit'] for dfs in all_dfs.values()], axis=0)

    df_all_global.to_excel(writer, sheet_name='Cumulative data', header=False, index=False, startrow=0, startcol=0)
    df_all_intersub.to_excel(writer, sheet_name='Cumulative data', index=False, startrow=len(df_all_global.index), startcol=0)
    df_all_sub.to_excel(writer, sheet_name='Cumulative data', index=False, startrow=len(df_all_global.index), startcol=len(df_all_intersub.columns))
