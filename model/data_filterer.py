import pandas as pd
import logging

import pandas.errors


class DataFilterer:
    def __init__(self, config, data_tuples):
        self.config = config
        self.data_tuples = data_tuples
        self.filters = self.get_filters()
        self.pivot_tables = []
        self.merged_table = None

    def loop_over(self):
        for current_tuple in self.data_tuples:
            self.map_team_names(current_tuple)
            filtered_data = self.filter_data(current_tuple)
            self.pivot_tables.append(
                self.convert_to_pivot(filtered_data, current_tuple[0]))
        self.aggregate_pivot_tables()

    def map_team_names(self, current_tuple):
        try:
            current_tuple[1][self.config['aggregateColumn']] = current_tuple[1][self.config['aggregateColumn']].apply(
                self.get_mapping)
        except ValueError as e:
            logging.error(e)
            exit(0)

    def get_mapping(self, team_name):
        team_mapping = self.config['teams']
        for team, names in team_mapping.items():  # search in each array  for the desired team names
            try:
                if team_name in names['aliases']:
                    return team  # if the name is found, return the mapping
            except KeyError as e:
                logging.error(f"{e} is not defined for team {team_name}.")
                exit(0)
        raise ValueError("Team '" + team_name + "' has no mapping")

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
        except pandas.errors.UndefinedVariableError as e:
            logging.error(f"Filter with {e} in the table {current_tuple[0]}.")
            exit(0)
        if filtered_data.empty:
            logging.warning(
                f'After filtering, the table {current_tuple[0]} is empty, make sure all filters are correct.')
        return filtered_data

    def get_filters(self):
        filters_by_filename = {}
        # Loop over the filenames and retrieve the filters for each one
        for filename in self.config["filenames"]:
            try:
                filters_by_filename[filename] = self.config[filename]["filters"]
            except KeyError as e:
                if e.args[0] == 'filters':
                    logging.error(f"The 'filters' field is not defined for {filename} configuration")
                    exit(0)
                logging.error("{} does not have a configuration defined in the file.".format(e))
                exit(0)
        return filters_by_filename

    def convert_to_pivot(self, filtered_data, filename):
        try:
            index_columns = [self.config['aggregateColumn']]
            values_columns = list(self.config[filename]['values'].keys())
            aggfuncs = {}
            fill_values = {}
            for col, settings in self.config[filename]['values'].items():
                aggfuncs[col] = settings['aggfunc']
                fill_values[col] = settings['fill_value']

            # pivot table without the preference filter
            pivot_table = self.return_pivot(aggfuncs, fill_values, filtered_data, index_columns,
                                            values_columns,filename)
        except KeyError as e:
            logging.error(f"Could not find field {e} in configuration file for table {filename}.")
            exit(0)
        except Exception as e:
            logging.error(e)
            exit(0)

        # now we try to pivot with the preference filter
        try:
            filter_name = self.config[filename]['preference_filter']
            value_name = self.config[filename]['preference_value']
            filtered_data = filtered_data[(
                    filtered_data[filter_name] == value_name)]
            filtered_pivot = self.return_pivot(aggfuncs, fill_values, filtered_data, index_columns,
                                               values_columns, filename).add_prefix('Total ')
            pivot_table = pd.concat([pivot_table, filtered_pivot], axis=1)
        except KeyError as e:
            logging.warning(f"The table {filename} does not have a {e} set.")

        return pivot_table

    @staticmethod
    def return_pivot(aggfuncs, fill_values, filtered_data, index_columns, values_columns, filename):
        try:
            result = pd.pivot_table(filtered_data,
                                    index=index_columns,
                                    values=values_columns,
                                    aggfunc=aggfuncs,
                                    fill_value=fill_values)
        except TypeError:
            logging.error(f"The settings for the {values_columns} of {filename} are wrong.")
            exit(0)
        if result is None:
            logging.error(f"The settings for the {values_columns} of {filename} appear to be good, but could not "
                          f"generate a pivot table")
            exit(0)
        return result

    def aggregate_pivot_tables(self):
        self.merged_table = pd.DataFrame(
            columns=[self.config['aggregateColumn']])
        for table in self.pivot_tables:
            try:
                self.merged_table = pd.merge(
                    self.merged_table, table, on=self.config['aggregateColumn'], how='outer')
            except TypeError:
                logging.error(f"Could not merge the table {table}")
        self.merged_table.fillna(0, inplace=True)
