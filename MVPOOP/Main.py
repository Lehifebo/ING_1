import DataFilterer as dataFilter
import pandas as pd
import json
with open('D:\GitHub\SoftEng\MVPOOP\config.json') as f:
            config = json.load(f)

data=dataFilter.DataFilterer('',config, pd.read_csv('D:\GitHub\SoftEng\merged_tables.csv'))
data.map_team_names()
data.filter_data()
data.convert_to_pivot()

print(data.pivot_table)
