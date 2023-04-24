import pandas as pd


class DataFilterer:
    def __init__(self, path, config, df):
        self.path = path #specify path of what or itll get confuding
        self.config = config
        self.all_data = df  # maybe file instead
        self.filtered_data = None
        self.filtered_columns = None
        self.pivot_table = None

    def map_team_names(self):
        try:
            self.all_data['CI Config Admin Group'] = self.all_data['CI Config Admin Group'].apply(self.get_mapping)
        except ValueError as e:
            print(e)
            exit(0)
    def get_mapping(self,team_name):
        team_mapping = self.config['teams']
        for team, names in team_mapping.items(): #search in each array  for the desired team names
            if team_name in names:
                return team #if the name is found, return the mapping
        raise ValueError("Team '" +team_name + "' has no mapping")
    
    def filter_columns(self):
        try:
            columns = self.config['columns']
            self.filtered_columns = self.filtered_data[columns]
        except KeyError as e:
            print("Could not find key '{}' in config file.".format(e))
            exit(0)
    
    def filter_data(self):
        filters_df = pd.DataFrame.from_dict(self.config['filters'], orient='index', columns=['value'])
        filters_df['query_string'] ="(`"+ filters_df.index + "`"+ " == '" + filters_df['value'] + "'"+" | `"+ filters_df.index + "`"+ " == 'NaN')"
        query = ' & '.join(filters_df['query_string']).replace("'False'", "False").replace("'True'", "True")
        self.all_data=self.all_data.fillna("NaN")#convert from pandas obj NaN to string
        print(query)
        self.filtered_data = self.all_data.query(query)

    def convert_to_pivot(self):
        try:
            index_columns = [self.config['aggregateColumn']]
            values_columns = list(self.config['values'].keys())
            aggfuncs = {}
            fill_values = {}
            for col, settings in self.config['values'].items():
                aggfuncs[col] = settings['aggfunc']
                fill_values[col] = settings['fill_value']
            margins = self.config.get('margins', True)

            self.pivot_table = pd.pivot_table(self.filtered_data,
                                            index=index_columns,
                                            values=values_columns,
                                            aggfunc=aggfuncs,
                                            fill_value=fill_values,
                                            margins=margins,
                                            dropna=self.config.get('dropna', True))
        except KeyError as e:
            print("Could not find key '{}' in config file.".format(e))
            exit(0)


