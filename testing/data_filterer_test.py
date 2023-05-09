import unittest
import sys
import pandas as pd
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.data_filterer import DataFilterer as df

#Not working, waiting until the datafilterer is in a more stable state.
class TestDataFilterer(unittest.TestCase):

    def test_map_team_names(self):
        # Create a mock configuration with team name aliases
        config = {
            'teams': {
                'Team A': {'aliases': ['A', 'Team A']},
                'Team B': {'aliases': ['B', 'Team B']},
                'Team C': {'aliases': ['C', 'Team C']},
                'Team D': {'aliases': ['D', 'Team D']}
            }
        }

        # Create a mock data tuple with a DataFrame containing team names
        data = pd.DataFrame({
            'CI Config Admin Group': ['A', 'Team B', 'C', 'Team D']
        })
        # Create a DataFilterer instance and call the map_team_names method
        filterer = df.DataFilterer(config, [(0, data)])

        filterer.map_team_names((0, data))

        # Check that the team names have been mapped correctly
        expected_output = pd.DataFrame({
            'CI Config Admin Group': ['Team A', 'Team B', 'Team C', 'Team D']
        })
        pd.testing.assert_frame_equal(data, expected_output)

    def test_get_mapping_with_valid_team_name(self):
        # Create a mock configuration with team name aliases
        config = {
            'teams': {
                'Team A': {'aliases': ['A', 'Team A']},
                'Team B': {'aliases': ['B', 'Team B']},
                'Team C': {'aliases': ['C', 'Team C']},
                'Team D': {'aliases': ['D', 'Team D']}
            }
        }

        # Create a DataFilterer instance and call the get_mapping method with a valid team name
        filterer = df.DataFilterer(config, [])
        mapping = filterer.get_mapping('C')

        # Check that the mapping is correct
        self.assertEqual(mapping, 'Team C')

    def test_get_mapping_with_invalid_team_name(self):
        # Create a mock configuration with team name aliases
        config = {
            'teams': {
                'Team A': {'aliases': ['A', 'Team A']},
                'Team B': {'aliases': ['B', 'Team B']},
                'Team C': {'aliases': ['C', 'Team C']},
                'Team D': {'aliases': ['D', 'Team D']}
            }
        }

        # Create a DataFilterer instance and call the get_mapping method with an invalid team name
        filterer = df.DataFilterer(config, [])
        with self.assertRaises(ValueError):
            filterer.get_mapping('Invalid Team Name')

    def test_filter_data(self):
        # Create a mock configuration with filter criteria for the file
        config = {
            'filenames': ['amumu'],
            'amumu': {
                'filters': {
                    'column1': 'value1',
                    'column2': 'value2'
                }
            }
        }

        # Create a mock data tuple with a DataFrame containing data
        data = pd.DataFrame({
            'filenames': ['amumu', 'amumu', 'amumu', 'amumu']
        })

        # Create a DataFilterer instance and call the get_filters method
        filterer = df.DataFilterer(config, [(0, data)])
        filterer.get_filters()
        print((0, data))

        # Call the filter_data method to filter the data
        filtered_data = filterer.filter_data((0, data))

        # Check that the filtered data has the expected values
        expected_output = pd.DataFrame({
            'column1': ['value1', 'value1'],
            'column2': ['value2', 'value1'],
        })
        pd.testing.assert_frame_equal(filtered_data, expected_output)


# Create a test suite and add the TestDataFilterer test class to it
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDataFilterer))

# Run the test suite and display the results in the console
runner = unittest.TextTestRunner()
result = runner.run(suite)
