import os
import pandas as pd
from datetime import datetime

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get the path to the Reports directory relative to the MVPOOP directory
hist_dir = os.path.join(project_dir, "historical_data")


class Team:
    def __init__(self, emailing_list, report, team_name, hist_data_path):
        # Initialize the Team object with the emailing list, report, team name, and historical data path
        self.emailing_list = emailing_list
        self.report = report
        self.historical_data = None
        self.team_name = team_name
        self.hist_data_path = hist_data_path
        self.path = None

    def add_to_history(self, report):
        # Add the current report to the team's historical data
        append = self.team_name + "_data.csv"
        columns = []

        # Extract columns from each report
        [columns.extend(list(data.columns)) for (name, data) in report]
        self.path = self.hist_data_path + append

        try:
            self.historical_data = pd.read_csv(self.path)
        except FileNotFoundError:
            self.historical_data = pd.DataFrame(columns=columns)

        data = pd.DataFrame(columns=columns)
        row = []

        # Sum each column in the report and append it to the row
        for (name, table) in report:
            for column in list(table.columns):
                column_sum = table[column].sum()
                row.append(column_sum)

        data.loc[0] = row
        data['Date'] = datetime.now().date()
        data['CI Config Admin Group'] = self.team_name

        # Concatenate the current report data with the historical data and save it to the file
        self.historical_data = pd.concat([self.historical_data, data], ignore_index=True)
        self.historical_data.to_csv(self.path, index=False)
