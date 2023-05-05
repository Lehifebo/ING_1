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

    # maybe put a try catch that tries to open the file and do everything else create the file and do everything
    def add_to_history(self, report):
        mvpoop_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        hist_dir = os.path.join(
            mvpoop_dir, "HistoricalData", self.team_name, "\_data.csv")
        if os.path.exists(hist_dir):  # probs use try catch instead
            self.historical_data = pd.read_csv(hist_dir)
            report['Date'] = datetime.now().date()
            self.historical_data = pd.concat(
                [self.historical_data, report.to_frame().T], ignore_index=True)
            self.historical_data.to_csv(hist_dir, index=False)
        else:
            report['Date'] = datetime.now().date()
            data = pd.DataFrame(columns=[
                                'CI Config Admin Group', 'Compliance result ID', 'Vulnerability ID', 'Date'])
            self.historical_data = pd.concat(
                [data, report.to_frame().T], ignore_index=True)
            self.historical_data.to_csv(hist_dir, index=False)
