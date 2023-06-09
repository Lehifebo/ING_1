import unittest
import os
import pandas as pd
from pipeline_module.data.team import Team


# Define the unit test class
class TestTeam(unittest.TestCase):
    def setUp(self):
        # Set up the necessary data and objects for testing
        self.emailing_list = ["example1@example.com", "example2@example.com"]
        self.report = [("Table1", pd.DataFrame({'column1': [1, 2, 3], 'column2': [4, 5, 6]})),
                       ("Table2", pd.DataFrame({'column3': [7, 8, 9]}))]
        self.team_name = "team1"
        self.hist_data_path = "D:/GitHub/SoftEng/SoftEng/testing/test_files/"

        self.team = Team(self.emailing_list, self.report, self.team_name, self.hist_data_path)

    def test_add_to_history(self):
        # Test the 'add_to_history' method
        # Call the add_to_history method
        self.team.add_to_history(self.report)

        # Check if the historical data file was created
        self.assertTrue(os.path.exists(self.team.path))

        # Check if the historical data file has the expected columns
        expected_columns = ['column1', 'column2', 'column3', 'Date', 'CI Config Admin Group']
        historical_data = pd.read_csv(self.team.path)
        self.assertListEqual(list(historical_data.columns), expected_columns)


if __name__ == '__main__':
    unittest.main()
