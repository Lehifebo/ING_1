import os
import pandas as pd


class Team:
    def __init__(self, emailing_list, report, team_name):
        self.emailing_list = emailing_list
        self.report = report
        self.historical_data = None
        self.team_name = team_name
        self.path = None

    def add_to_history(self, report):
        self.path = "../HistoricalData/" + self.team_name + "_data.csv"  # path should be a field
        if os.path.exists(self.path): # probs use try catch instead
            print("error    ")
            self.historical_data = pd.read_csv(self.path)
            #print(type(self.historical_data))
            self.historical_data = pd.concat([self.historical_data, report.to_frame().T], ignore_index=True)
            self.historical_data.to_csv(self.path)
        else:
            print("test")
            print(report)
            print(type(report))
            data = pd.DataFrame(columns=['CI Config Admin Group', 'Compliance result ID', 'Vulnerability ID'])
            self.historical_data = pd.concat([data, report.to_frame().T], ignore_index=True)
            self.historical_data.to_csv(self.path,index=False)
