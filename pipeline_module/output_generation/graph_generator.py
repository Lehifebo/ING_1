import pandas as pd
import matplotlib.pyplot as plt
import os

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class GraphGenerator:
    def __init__(self, teams, graph_path):
        # Initialize the GraphGenerator object
        self.teams = teams
        self.graph_path = graph_path

    @staticmethod
    def fix_date(data):
        # Convert the 'Date' column to a datetime object and set it as the index
        data['Date'] = pd.to_datetime(data['Date'])
        data['Date'] = data['Date'].dt.strftime('%m-%d')
        data.set_index('Date', inplace=True)
        return data

    def create_team_graphs(self):
        # Create graphs for each team and save them as images
        for team in self.teams:
            fig = self.team_graph(team)
            fig.savefig(self.graph_path + team.team_name + "_graph.png")

    def team_graph(self, team):
        # Create a graph for a specific team
        data = team.historical_data
        data = self.fix_date(data)
        columns = data.columns.to_list()

        # Create a figure and axis object
        fig, ax = plt.subplots()

        # Remove the last column from the list (assuming it's not needed for the graph)
        columns.pop()
        issues = columns

        # Plot each issue's data on the graph
        for issue in issues:
            data[issue].plot(ax=ax, label=issue)

        # Set the title, legend, and axis labels
        ax.set_title('Issues for team ' + team.team_name)
        ax.legend()
        ax.set_xlabel('Date')
        ax.set_ylabel('Count')
        return fig

    def create_tribe_lead_graphs(self, issues):
        # Create graphs for each issue and save them as images
        for issue in issues:
            fig = self.issue_graph(issue)
            fig.savefig(self.graph_path + "tl_graphs/tl_" + issue + "_graph.png")

    def tribe_lead_graph(self):
        # Generate a graph for the tribe lead
        datasets = self.get_data_tuple()

        # Plot the sum of values for each dataset on the same graph
        for config, data in datasets:
            sum_values = data["s"].sum(axis=1)
            plt.plot(sum_values, label=config)

        # Set the x and y labels, and show the legend
        plt.xlabel('Date')
        plt.ylabel("Sum of values")
        plt.legend()
        plt.show()

    def get_data_tuple(self):
        # Retrieve the data tuples for each team
        datasets = []
        for team in self.teams:
            config_name = team.team_name
            historical_data = team.historical_data
            historical_data = self.fix_date(historical_data)
            datasets.append((config_name, historical_data))
        return datasets

    def issue_graph(self, issue):
        # Generate a graph for a specific issue
        fig, ax = plt.subplots()

        # Plot the data for each team related to the issue on the same graph
        for team in self.teams:
            ax.plot(team.historical_data[issue], label=team.team_name)

        # Set the x and y labels, and show the legend
        ax.set_xlabel('Date')
        ax.set_ylabel(issue)
        ax.legend()
        return fig
