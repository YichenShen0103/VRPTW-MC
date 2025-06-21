import pandas as pd

dfs = pd.read_excel('data/data_v2.0.xlsx', sheet_name=None)

# Extract the sheet by sheet name
ss_df = dfs['库站运距']
for i in range(len(ss_df)):
    station1 = "D" + str(ss_df.iloc[i, 0] % 100)
    station2 = chr(ss_df.iloc[i, 2] % 100 - 1 + ord('A'))
    cost = ss_df.iloc[i, 4]
    print("{ data: { id: \"" + station1 + station2 + "\", source: \""+ station1 + "\", target: \"" + station2 + "\", weight: " + str(cost) + "} },")

