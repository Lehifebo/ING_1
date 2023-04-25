import os
import DataFilterer as dataFilter
import pandas as pd
import json
import FileReader as fr

reader = fr.FileReader('Reports')
data_tuples=reader.getExcels()

relative_path_json = '../Reports/configuration.json'
# relative_path_tables_folder = 'merged_tables.csv' 
# # Get the absolute path of the JSON file by joining the relative path with the current file's directory

absolute_path_json = os.path.join(os.path.dirname(__file__), relative_path_json)
# absolute_path_tables_folder = os.path.join(os.path.dirname(__file__), relative_path_tables_folder)

with open(absolute_path_json) as f:
            config = json.load(f)
filterer = dataFilter.DataFilterer(config,data_tuples)
filterer.get_filters()

filterer.loop_over()
print(filterer.merged_table)


# data=dataFilter.DataFilterer('',config, pd.read_csv(absolute_path_tables_folder))
# data.map_team_names()
# data.filter_data()
# data.convert_to_pivot()

