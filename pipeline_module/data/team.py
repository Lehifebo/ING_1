import os
import pandas as pd
from datetime import datetime

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get the path to the Reports directory relative to the MVPOOP directory
hist_dir = os.path.join(project_dir, "historical_data")


class Team:
    def __init__(self, emailing_list, report, team_name, hist_data_path):
        self.emailing_list = emailing_list
        self.report = report
        self.historical_data = None
        self.team_name = team_name
        self.hist_data_path = hist_data_path
        self.path = None

    def add_to_history(self, report):
        append = self.team_name+"_data.csv"
        columns = []
        [columns.extend(list(data.columns)) for (name, data) in report]
        #columns = report.index  # maybe from a config file
        self.path = self.hist_data_path+append
        try:
            self.historical_data = pd.read_csv(self.path)
        except FileNotFoundError:
            self.historical_data = pd.DataFrame(columns=columns)
        data = pd.DataFrame(columns=columns)
        row = []
        for (name, table) in report:
            for column in list(table.columns):
                column_sum = table[column].sum()
                row.append(column_sum)
        data.loc[0] = row
        #print("test")
        #print(type(data))
        #quit()
        data['Date'] = datetime.now().date()
        data['CI Config Admin Group'] = self.team_name
        self.historical_data = pd.concat([self.historical_data, data], ignore_index=True)
        self.historical_data.to_csv(self.path, index=False)
