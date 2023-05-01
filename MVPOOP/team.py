import os
import pandas as pd


class Team:
    def __init__(self, emailing_list, report):
        self.emailing_list = emailing_list
        self.report = report
        self.historical_data = None
        self.team_name = "test"  # needs to be passed

    def add_to_history(self, report):
        path = "../HistoricalData/" + self.team_name + "_data.csv"  # path should be a field
        if os.path.exists(path):
            self.historical_data = pd.read_csv(path)
            print(type(self.historical_data))
            self.historical_data = pd.concat([self.historical_data, report])
            self.historical_data.to_csv(path)
        else:
            print(report)
            data = pd.DataFrame(report)
            print()
            print(data)
            data.to_csv(path)
