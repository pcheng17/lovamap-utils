import pandas as pd

input_file = "./stats_spheres_100_interior_surroundingBeads.xlsx"
output_file = "./output.xlsx"

# DO NOT TOUCH ANYTHING BELOW THIS LINE

excel = pd.ExcelFile(input_file)

# Dictionary of dataframes by sheet name
df_per_particle_count = {sheet: excel.parse(sheet) for sheet in excel.sheet_names}

# Get column names from the first sheet
descriptors = df_per_particle_count[excel.sheet_names[0]].columns.values

# For every name in descriptors, create a new dataframe that contains
# only the column with that name from each of the sheets
df_per_descriptor = {}
for name in descriptors:
    df_per_descriptor[name] = pd.concat([df_per_particle_count[sheet][name] for sheet in df_per_particle_count], \
        keys=excel.sheet_names, axis=1)

with pd.ExcelWriter(output_file) as writer:
    for name, df in df_per_descriptor.items():
        short_name = name[:30] if len(name) > 30 else name
        df.to_excel(writer, sheet_name=short_name, index=False)
