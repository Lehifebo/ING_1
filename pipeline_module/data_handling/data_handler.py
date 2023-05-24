import logging

import pandas as pd

from .data_filterer import DataFilterer
from .file_reader import FileReader
from pipeline_module.data.team import Team


class DataHandler:
    def __init__(self, input_path, config, hist_data_path):
        self.input_path = input_path
        self.file_reader = FileReader(input_path)
        self.config = config
        self.data_filterer = None
        self.merged_table = None
        self.hist_data_path = hist_data_path

    def handle_data(self):
        data_tuples = self.file_reader.get_excels()
        self.data_filterer = DataFilterer(self.config, data_tuples)
        self.merged_table = self.data_filterer.filter_files()

    def generate_teams(self):
        teams = []
        team_dict = self.config['teams']
        team_names = list(team_dict.keys())


        for index, row in self.merged_table.iterrows():
            print(row)
            try:
                team = Team(team_dict[row[0]]['email_list'], row, team_names[index], self.hist_data_path)
                teams.append(team)
                team.add_to_history(row)
            except KeyError as e:
                logging.error(f"{e} is missing for team {team_names[index]}")
                exit(0)
        return teams
