import unittest
import os

import pandas as pd
from pipeline_module.output_generation.graph_generator import GraphGenerator

from pipeline_module.data.team import Team


# Define the unit test class
class TestGraphGenerator(unittest.TestCase):
    def setUp(self):
        # Set up the necessary data and objects for testing
        team_name = "Guardians"
        hist_data_path = "D:/GitHub/SoftEng/SoftEng/testing/test_files/historical_data.csv"
        emailing_list = ["test1@test", "test2@test"]
        team = Team(emailing_list, None, team_name, hist_data_path)
        team.historical_data = pd.read_csv(team.hist_data_path)
        self.teams = [team]
        self.graph_path = "D:/GitHub/SoftEng/SoftEng/testing/test_files/"

    def test_fix_date(self):
        # Test the 'fix_date' method
        data = pd.DataFrame({
            'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'Count': [10, 15, 12]
        })
        graph_generator = GraphGenerator(self.teams, self.graph_path)
        fixed_data = graph_generator.fix_date(data)
        self.assertEqual(fixed_data.index.to_list(), ['01-01', '01-02', '01-03'])

    def test_team_graph(self):
        # Test the 'team_graph' method
        team = self.teams[0]
        graph_generator = GraphGenerator([team], self.graph_path)
        fig = graph_generator.team_graph(team)

        # Validate the properties of the generated figure
        ax = fig.axes[0]
        self.assertEqual(ax.get_xlabel(), "Date")
        self.assertEqual(ax.get_ylabel(), "Count")
        self.assertEqual(ax.get_title(), 'Issues for team ' + team.team_name)

    def test_create_team_graphs(self):
        # Test the 'create_team_graphs' method
        team = self.teams[0]
        graph_generator = GraphGenerator(self.teams, self.graph_path)
        graph_generator.create_team_graphs()

        # Check if the graph file has been created
        self.assertTrue(os.path.exists(graph_generator.graph_path + team.team_name + "_graph.png"))
        os.remove("D:/GitHub/SoftEng/SoftEng/testing/test_files/" + team.team_name + "_graph.png")

    def test_create_tribe_lead_graphs(self):
        # Test the 'create_tribe_lead_graphs' method
        issues = ['Issue Overdue']
        issue = issues[0]
        graph_generator = GraphGenerator(self.teams, self.graph_path)
        graph_generator.create_tribe_lead_graphs(issues)

        # Check if the tribe lead graph file has been created
        self.assertTrue(
            os.path.exists("D:/GitHub/SoftEng/SoftEng/testing/test_files/tl_graphs/" + "tl_" + issue + "_graph.png"))
        os.remove("D:/GitHub/SoftEng/SoftEng/testing/test_files/tl_graphs/" + "tl_" + issue + "_graph.png")

    def test_issue_graph(self):
        # Test the 'issue_graph' method
        issue = "Issue Overdue"
        graph_generator = GraphGenerator(self.teams, self.graph_path)
        fig = graph_generator.issue_graph(issue)

        # Validate the properties of the generated figure
        ax = fig.axes[0]
        self.assertEqual(ax.get_xlabel(), "Date")
        self.assertEqual(ax.get_ylabel(), issue)

        num_teams = len(self.teams)
        plotted_lines = ax.get_lines()
        self.assertEqual(len(plotted_lines), num_teams)

        team_names = [team.team_name for team in self.teams]
        plotted_labels = [line.get_label() for line in plotted_lines]
        self.assertListEqual(plotted_labels, team_names)


if __name__ == '__main__':
    unittest.main()
