import os
import pandas as pd
from datetime import datetime


class Team:
    def __init__(self, emailing_list, report, team_name):
        self.emailing_list = emailing_list
        self.report = report
        self.historical_data = None
        self.team_name = team_name
        self.path = None

    def add_to_history(self, report):
        columns = ['CI Config Admin Group', 'Compliance result ID',
                   'Vulnerability ID', 'Total Vulnerability ID', 'Date']  # maybe from a config file
        self.path = "../historical_data/" + self.team_name + "_data.csv"
        try:
            self.historical_data = pd.read_csv(self.path)
        except FileNotFoundError:
            self.historical_data = pd.DataFrame(columns=columns)

        report['Date'] = datetime.now().date()
        self.historical_data = pd.concat([self.historical_data, report.to_frame().T], ignore_index=True)
        self.historical_data.to_csv(self.path, index=False)
