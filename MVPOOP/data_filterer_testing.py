import unittest

import pandas as pd


import data_filterer as df


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
            'CI Config Admin Group': ['A', 'Team B', 'C','Team D']
        })
        
        # Create a DataFilterer instance and call the map_team_names method
        filterer = df.DataFilterer(config, [(0, data)])
        filterer.map_team_names((0, data))
        
        # Check that the team names have been mapped correctly
        expected_output = pd.DataFrame({
            'CI Config Admin Group': ['Team A', 'Team B', 'Team C', 'Team D']
        })
        pd.testing.assert_frame_equal(data, expected_output)


    

# Create a test suite and add the TestDataFilterer test class to it
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDataFilterer))

# Run the test suite and display the results in the console
runner = unittest.TextTestRunner()
result = runner.run(suite)

    