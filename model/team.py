import os
import pandas as pd
from datetime import datetime

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get the path to the Reports directory relative to the MVPOOP directory
hist_dir = os.path.join(project_dir, "historical_data")


class Team:
    def __init__(self, emailing_list, report, team_name):
        self.emailing_list = emailing_list
        self.report = report
        self.historical_data = None
        self.team_name = team_name
        self.path = None

    def add_to_history(self, report):
        append = self.team_name+"_data.csv"
        #print(report.index)
        columns = report.index  # maybe from a config file
        self.path = os.path.join(hist_dir, append)
        try:
            self.historical_data = pd.read_csv(self.path)
        except FileNotFoundError:
            self.historical_data = pd.DataFrame(columns=columns)

        report['Date'] = datetime.now().date()
        self.historical_data = pd.concat([self.historical_data, report.to_frame().T], ignore_index=True)
        self.historical_data.to_csv(self.path, index=False)
