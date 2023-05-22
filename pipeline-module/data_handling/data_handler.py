import logging

import data_filterer as df
import file_reader as fr
from ..data import team as t


class DataHandler:
    def __init__(self, input_path, config):
        self.input_path = input_path
        self.file_reader = fr.FileReader(input_path)
        self.config = config
        self.data_filterer = None
        self.merged_table = None

    def handle_data(self):
        data_tuples = self.file_reader.get_excels()
        self.data_filterer = df.DataFilterer(self.config, data_tuples)
        self.merged_table = self.data_filterer.filter_files()

    def generate_teams(self):
        teams = []
        team_dict = self.config['teams']
        team_names = list(team_dict.keys())
        for index, row in self.merged_table.iterrows():
            try:
                team = t.Team(team_dict[row[0]]['email_list'], row, team_names[index])
                teams.append(team)
                team.add_to_history(row)
            except KeyError as e:
                logging.error(f"{e} is missing for team {team_names[index]}")
                exit(0)
        return teams
