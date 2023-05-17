import pandas as pd
import matplotlib.pyplot as plt
import os

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class GraphGenerator:
    def __init__(self, teams):
        self.teams = teams

    @staticmethod
    def fix_date(data):
        # Convert the 'Date' column to a datetime object
        data['Date'] = pd.to_datetime(data['Date'])
        data['Date'] = data['Date'].dt.strftime('%m-%d')
        # Set the 'Date' column as the index
        data.set_index('Date', inplace=True)
        return data

    def create_team_graphs(self):
        for team in self.teams:
            fig = self.team_graph(team)
            fig.savefig(os.path.join(os.path.join(project_dir, "output/graphs"),team.team_name+"graph.png"))

    def team_graph(self, team):
        data = team.historical_data
        data = self.fix_date(data)
        columns = data.columns.to_list()
        # Create a figure and axis object
        fig, ax = plt.subplots()
        issues = columns[1:]
        for issue in issues:
            data[issue].plot(ax=ax, label=issue)
        # Set the title, legend, and axis labels
        ax.set_title('Issues for team ' + team.team_name)
        ax.legend()
        ax.set_xlabel('Date')
        ax.set_ylabel('Count')
        return fig

    def get_data_tuples(self):
        datasets = []
        for x in range(1, 11):
            config_name = "Config{:04d}".format(x)
            historical_data = pd.read_csv("../historical_data/" + config_name + "_data.csv")
            historical_data = self.fix_date(historical_data)
            datasets.append((config_name, historical_data))
        return datasets

    def issue_graph(self, issue):
        # issue = 'Vulnerability ID'
        datasets = self.get_data_tuples()
        for config, data in datasets:
            # plot the 'y' column from both dataframes on the same graph
            plt.plot(data[issue], label=config)
            # add labels and legend
        plt.xlabel('Date')
        plt.ylabel(issue)
        plt.legend()

        # show the graph
        plt.show()

    def everything_graphs(self):
        datasets = self.get_data_tuples()
        issues = ['Compliance result ID',
                  'Vulnerability ID', 'Total Vulnerability ID']
        fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(20, 8))
        for index, issue in enumerate(issues):
            # maybe here could use issue function but difference with axs
            for config, data in datasets:
                # plot the 'y' column from both dataframes on the same graph
                axs[index].plot(data[issue], label=config)
                # add labels and legend
            plt.xlabel('Date')
            plt.ylabel(issue)
            plt.legend()

            # show the graph
        plt.show()
