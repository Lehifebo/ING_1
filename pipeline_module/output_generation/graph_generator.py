import pandas as pd
import matplotlib.pyplot as plt
import os

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GraphGenerator:
    def __init__(self, teams,graph_path):
        self.teams = teams
        self.graph_path = graph_path

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
            fig.savefig(self.graph_path + team.team_name + "_graph.png")

    def team_graph(self, team):
        data = team.historical_data
        data = self.fix_date(data)
        columns = data.columns.to_list()
        # Create a figure and axis object
        fig, ax = plt.subplots()
        columns.pop()
        issues = columns
        for issue in issues:
            data[issue].plot(ax=ax, label=issue)
        # Set the title, legend, and axis labels
        ax.set_title('Issues for team ' + team.team_name)
        ax.legend()
        ax.set_xlabel('Date')
        ax.set_ylabel('Count')
        return fig

    def create_tribe_lead_graphs(self, issues):
        for issue in issues:
            fig = self.issue_graph(issue)
            fig.savefig(self.graph_path + "tl_"+issue+"_graph.png")
    def tribe_lead_graph(self, issue):

        datasets = self.get_data_tuple()
        for config, data in datasets:
            sum_values = data["s"].sum(axis=1)
            plt.plot(sum_values, label=config)
        plt.xlabel('Date')
        plt.ylabel("Sum of values")
        plt.legend()

        # show the graph
        plt.show()

    def get_data_tuple(self):
        datasets = []
        for team in self.teams:
            config_name = team.team_name
            historical_data = team.historical_data
            historical_data = self.fix_date(historical_data)
            datasets.append((config_name, historical_data))
        return datasets

    def issue_graph(self,issue):
        fig, ax = plt.subplots()
        for team in self.teams:
            # plot the 'y' column from both dataframes on the same graph
            ax.plot(team.historical_data[issue],  label=team.team_name)
            # add labels and legend
        ax.set_xlabel('Date')
        ax.set_ylabel(issue)
        ax.legend()
        return fig


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
