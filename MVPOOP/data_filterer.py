import pandas as pd


class DataFilterer:
    def __init__(self, config, data_tuples):
        self.config = config
        self.data_tuples = data_tuples
        self.filters = None
        self.pivot_tables = []
        self.merged_table = None

    def loop_over(self):
        for tuple in self.data_tuples:
            self.map_team_names(tuple)
            filtered_data = self.filter_data(tuple)
            self.pivot_tables.append(self.convert_to_pivot(filtered_data, tuple[0]))
        self.aggregate_pivot_tables()

    def map_team_names(self, tuple):
        try:
            tuple[1]['CI Config Admin Group'] = tuple[1]['CI Config Admin Group'].apply(self.get_mapping)
        except ValueError as e:
            print(e)
            exit(0)

    def get_mapping(self, team_name):
        team_mapping = self.config['teams']
        for team, names in team_mapping.items():  # search in each array  for the desired team names
            if team_name in names['aliases']:
                return team  # if the name is found, return the mapping
        raise ValueError("Team '" + team_name + "' has no mapping")

    def filter_data(self, tuple):
        filter = self.filters[tuple[0]]
        filters_df = pd.DataFrame.from_dict(filter, orient='index', columns=['value'])
        filters_df['query_string'] = "(`" + filters_df.index + "`" + " == '" + filters_df[
            'value'] + "'" + " | `" + filters_df.index + "`" + " == 'NaN')"
        query = ' & '.join(filters_df['query_string']).replace("'False'", "False").replace("'True'",
                                                                                           "True")  # map strings
        # True and False to actual booleans
        return tuple[1].query(query)

    def get_filters(self):
        filters_by_filename = {}
        # Loop over the filenames and retrieve the filters for each one
        for filename in self.config["filenames"]:
            filters_by_filename[filename] = self.config[filename]["filters"]
        self.filters = filters_by_filename

    def convert_to_pivot(self, data, filename):
        try:
            index_columns = [self.config['aggregateColumn']]
            values_columns = list(self.config[filename]['values'].keys())
            aggfuncs = {}
            fill_values = {}
            for col, settings in self.config[filename]['values'].items():
                aggfuncs[col] = settings['aggfunc']
                fill_values[col] = settings['fill_value']
            return pd.pivot_table(data,
                                  index=index_columns,
                                  values=values_columns,
                                  aggfunc=aggfuncs,
                                  fill_value=fill_values)
        except KeyError as e:
            print("Could not find key '{}' in config file.".format(e))
            exit(0)

    def aggregate_pivot_tables(self):
        self.merged_table = pd.DataFrame(columns=[self.config['aggregateColumn']])
        for table in self.pivot_tables:
            self.merged_table = pd.merge(self.merged_table, table, on=self.config['aggregateColumn'], how='outer')
        self.merged_table.fillna(0, inplace=True)
