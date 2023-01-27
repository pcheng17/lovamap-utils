import pandas as pd

input_file = "./stats_d_ellipsoids_interior.xlsx"
output_file = "./output.xlsx"

# Do not touch anything below this line

sheet_name = "Cumulative data"
volume_column_name = 'Volume_pL_'
target_column_name = 'x_SurroundingParticles'

df = pd.read_excel(io=input_file, sheet_name=sheet_name)

startRow = (df == volume_column_name).any(axis=1)
startIdx = df.index[startRow].tolist()

# Trim rows 
df = df.rename(columns=df.iloc[startIdx[0]])
df = df.tail(df.shape[0]-startIdx[0]-1)

# Trim columns
column_names = list(df.columns.values)
idx = column_names.index(volume_column_name)
df = df[df.columns[idx:]]

# Drop all rows that are completely NaN
df = df.dropna(how='all').reset_index(drop=True)

# Grab all valid numbers that we'll eventually partition by
valid_values = set(df[target_column_name].tolist())

# Partition dataframe via Lindsay's rule
new_dfs = []
for x in valid_values:
    new_dfs.append(df.loc[df[target_column_name] == x])

# Write all new dataframes to output file
with pd.ExcelWriter(output_file) as writer:
    for df, num in zip(new_dfs, valid_values):
        df.to_excel(writer, sheet_name=f'{num} neighbors', index=False)




