from pipeline_module.data_handling.data_filterer import DataFilterer
from pipeline_module.data_handling.file_reader import FileReader
from pipeline_module.data.team import Team


class DataHandler:
    def __init__(self, input_path, config, hist_data_path):
        # Initialize the DataHandler object with the input path, config, and historical data path
        self.input_path = input_path
        self.file_reader = FileReader(input_path)
        self.config = config
        self.data_filterer = None
        self.pivot_tables = None
        self.hist_data_path = hist_data_path

    def handle_data(self):
        # Handle the input data by reading and filtering it
        data_tuples = self.file_reader.get_excels()
        self.data_filterer = DataFilterer(self.config, data_tuples)
        self.pivot_tables = self.data_filterer.filter_files()

    def generate_teams(self):
        # Generate teams based on the filtered data
        teams = []
        team_dict = self.config['teams']
        team_names = list(team_dict.keys())

        # Iterate over the team names
        for team in team_names:
            file_reports = []

            # Iterate over the file-table tuples from the filtered data
            for file, table in self.pivot_tables:
                # Filter the table based on the current team
                report = table.loc[table.index.get_level_values('CI Config Admin Group') == team]
                file_reports.append((file, report))

            # Create a Team object
            team = Team(team_dict[team]['email_list'], file_reports, team, self.hist_data_path)

            # Add the file reports to the team's history
            team.add_to_history(file_reports)

            # Append the team to the list of teams
            teams.append(team)

        return teams
