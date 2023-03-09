import ntpath
import pandas as pd
import os

def merge_excel_files(excel_files, output_path: str) -> None:
    all_dfs = {}
    for file in excel_files:
        excel = pd.ExcelFile(file)
        all_dfs[file] = {sheet: excel.parse(sheet) for sheet in excel.sheet_names}

    with pd.ExcelWriter(os.path.join(output_path, 'merged.xlsx')) as writer:
        for file, dfs in all_dfs.items():
            # Take everything after the first underscore, but remove the extension.
            # Only take at most 30 characters.
            sheet_name = ntpath.basename(file).split('_', 1)[1].split('.', 1)[0]
            sheet_name = sheet_name[:30] if len(sheet_name) > 30 else sheet_name
            dfs['Global'].to_excel(writer, sheet_name=sheet_name, index=False, startrow=0, startcol=0)
            # Need +1 on the startrow index to account for the header row of the global dataframe.
            dfs['Intersub'].to_excel(writer, sheet_name=sheet_name, index=False, startrow=len(dfs['Global'].index)+1, startcol=0)
            dfs['Subunit'].to_excel(writer, sheet_name=sheet_name, index=False, startrow=len(dfs['Global'].index)+1, startcol=len(dfs['Intersub'].columns))

        # Write one final sheet of cumulated data
        df_all_global = pd.concat([dfs['Global'] for dfs in all_dfs.values()], axis=0)
        df_all_intersub = pd.concat([dfs['Intersub'] for dfs in all_dfs.values()], axis=0)
        df_all_sub = pd.concat([dfs['Subunit'] for dfs in all_dfs.values()], axis=0)

        df_all_global.to_excel(writer, sheet_name='Cumulative data', index=False, startrow=0, startcol=0)
        # Need +1 on the startrow index to account for the header row of the global dataframe.
        df_all_intersub.to_excel(writer, sheet_name='Cumulative data', index=False, startrow=len(df_all_global.index)+1, startcol=0)
        df_all_sub.to_excel(writer, sheet_name='Cumulative data', index=False, startrow=len(df_all_global.index)+1, startcol=len(df_all_intersub.columns))
