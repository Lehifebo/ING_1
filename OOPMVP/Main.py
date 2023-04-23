import DataFilterer as dataFilter
import pandas as pd
import json
with open('D:\GitHub\SoftEng\OOPMVP\config.json') as f:
            config = json.load(f)

data=dataFilter.DataFilterer('',config, pd.read_csv('D:\GitHub\SoftEng\merged_tables.csv'))
data.map_team_names()
print(data.df["CI Config Admin Group"])
