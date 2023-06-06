import unittest

import pandas as pd

from pipeline_module.output_generation.output_generator import OutputGenerator, StringGenerator, GraphGenerator
from pipeline_module.data.team import Team
from unittest.mock import MagicMock, patch


class TestOutputGenerator(unittest.TestCase):
    def setUp(self):
        team_name = "Guardians"
        hist_data_path = "../test_files/historical_data.csv"
        emailing_list = ["test1@test", "test2@test"]
        self.config = {
            'tribe_lead': 'tribe_lead@example.com',
            'issue_columns': ['issue1', 'issue2']
        }
        team = Team(emailing_list, [("aa", pd.DataFrame()),("aa", pd.DataFrame()),("aa", pd.DataFrame())], team_name, hist_data_path)
        self.teams = [team]
        self.output_generator = OutputGenerator(self.config,self.teams)

    def test_generate_string_output(self):
        config = {'tribe_lead': 'tribe_lead@example.com'}

        template_paths = ['../../configurations/template.txt', '../../configurations/template.txt']
        data_tuples = [('data1', pd.DataFrame()), ('data2', pd.DataFrame())]
        string_path = 'path/to/string.txt'

        # Create an instance of OutputGenerator with the config and teams
        output_generator = OutputGenerator(config, self.teams)

        # Mock the StringGenerator class
        with patch('pipeline_module.output_generation.string_generator.StringGenerator') as mock_string_generator:
            # Call the function to be tested
            output_generator.generate_string_output(template_paths, data_tuples, string_path)

            # Assert that the StringGenerator class was called with the expected arguments
            mock_string_generator.assert_called_once_with(template_paths, self.teams, 'tribe_lead@example.com', data_tuples)

    def test_generate_graph_output(self):
        graph_path = 'path/to/graphs/'

        output_generator = OutputGenerator(self.config, self.teams)
        output_generator.generate_graph_output(graph_path)

        # Add assertions to validate the existence of the generated graph files

if __name__ == '__main__':
    unittest.main()
