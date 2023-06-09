import pandas as pd
import logging

import pandas.errors


class DataFilterer:
    def __init__(self, config, data_tuples):
        self.config = config
        self.data_tuples = data_tuples
        self.filters = None
        self.pivot_tables = []

    def get_filters(self):
        filters_by_filename = {}
        # Loop over the filenames and retrieve the filters for each one
        for filename in self.config["filenames"]:
            try:
                filters_by_filename[filename] = self.config[filename]["filters"]
            except KeyError as e:
                if e.args[0] == 'filters':
                    raise KeyError (f"The 'filters' field is not defined for {filename} configuration")
                raise ValueError ("{} does not have a configuration defined in the file.".format(e))
        return filters_by_filename

    def filter_files(self):
        self.filters = self.get_filters()
        for current_tuple in self.data_tuples:
            self.map_team_names(current_tuple)
            filtered_data = self.filter_data(current_tuple)
            self.pivot_tables.append(
                self.convert_to_pivot(filtered_data, current_tuple[0]))
        return self.pivot_tables

    def map_team_names(self, current_tuple):
        try:
            current_tuple[1][self.config['aggregateColumn']] = current_tuple[1][self.config['aggregateColumn']].apply(
                self.get_mapping)
        except KeyError as e:
            raise KeyError(f"error with mapping team name : {e}")

    def get_mapping(self, team_name):
        team_mapping = self.config['teams']
        for team, names in team_mapping.items():  # search in each array  for the desired team names
            try:
                if team_name in names['aliases']:
                    return team  # if the name is found, return the mapping
            except Exception as e:
                raise KeyError(f"{e} is not defined for team {team_name}.")
        raise ValueError("ValueError: Team '" + team_name + "' has no mapping")

    def filter_data(self, current_tuple):
        current_filter = self.filters[current_tuple[0]]
        filters_df = pd.DataFrame.from_dict(
            current_filter, orient='index', columns=['value'])
        filters_df['query_string'] = "(`" + filters_df.index + "`" + " == '" + filters_df[
            'value'] + "'" + " | `" + filters_df.index + "`" + " == 'NaN')"
        # map strings True and False to actual booleans
        query = ' & '.join(filters_df['query_string']).replace(
            "'False'", "False").replace("'True'", "True")
        try:
            filtered_data = current_tuple[1].query(query)
            if filtered_data.empty:
                logging.warning(
                    f'After filtering, the table {current_tuple[0]} is empty, make sure all filters are correct.')
            return filtered_data
        except Exception as e:
            raise pandas.errors.UndefinedVariableError(f"Filter with {e} in the table {current_tuple[0]}.")

    def convert_to_pivot(self, filtered_data, filename):
        try:
            dictionary = self.config[filename]
            index_columns = dictionary['rows']
            values_columns = list(dictionary['values'].keys())
            aggfuncs = {}
            fill_values = {}
            for col, settings in dictionary['values'].items():
                aggfuncs[col] = settings['aggfunc']
                fill_values[col] = settings['fill_value']

            # pivot table without the preference filter
            pivot_table = self.return_pivot(aggfuncs, fill_values, filtered_data, index_columns,
                                            values_columns, filename)
            return filename, pivot_table
        except Exception as e:
            raise KeyError(f"Could not find field {e} in configuration file for table {filename}.")

    @staticmethod
    def return_pivot(aggfuncs, fill_values, filtered_data, index_columns, values_columns, filename):
        try:
            result = pd.pivot_table(filtered_data,
                                    index=index_columns,
                                    values=values_columns,
                                    aggfunc=aggfuncs,
                                    fill_value=fill_values,
                                    margins=True).fillna(0)
            return result
        except Exception:
            raise TypeError(f"The settings for the {values_columns} of {filename} are wrong.")

    def aggregate_pivot_tables(self):
        merged_table = pd.DataFrame(
            columns=[self.config['aggregateColumn']])
        for table in self.pivot_tables:
            try:
                merged_table = pd.merge(
                    merged_table, table, on=self.config['aggregateColumn'], how='outer')
            except Exception:
                raise TypeError(f"Could not merge the table {table}")
        merged_table.fillna(0, inplace=True)
        return merged_table
