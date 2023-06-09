import unittest
from unittest.mock import MagicMock
import pandas as pd
from pipeline_module.data_handling.data_handler import DataHandler


class TestDataHandler(unittest.TestCase):
    def setUp(self):
        self.input_path = 'D:/GitHub/SoftEng/SoftEng/testing/test_files/'
        self.config = {
            "teams": {
                "team1": {
                    "email_list": ["team1@example.com"]
                },
                "team2": {
                    "email_list": ["team2@example.com"]
                }
            }
        }
        self.hist_data_path = 'D:/GitHub/SoftEng/SoftEng/testing/test_files/'
        self.data_handler = DataHandler(self.input_path, self.config, self.hist_data_path)

    def test_generate_teams(self):
        pivot_tables = [('file1.xlsx', dataframe1), ('file2.xlsx', dataframe2)]
        self.data_handler.pivot_tables = pivot_tables

        team1_mock = MagicMock()
        team2_mock = MagicMock()

        team_mock = MagicMock()
        team_mock.return_value = team1_mock
        team_mock.side_effect = [team_mock, team2_mock]

        team1_add_to_history_mock = MagicMock()
        team2_add_to_history_mock = MagicMock()

        team1_mock.add_to_history = team1_add_to_history_mock
        team2_mock.add_to_history = team2_add_to_history_mock

        self.data_handler.Team = team_mock

        teams = self.data_handler.generate_teams()

        self.assertEqual(len(teams), 2)


# Sample dataframes for testing
data1 = {
    "CI Config Admin Group": ["team1", "team2", "team1"],
    "column1": ["value1", "value2", "value1"],
    "column2": [10, 20, 30],
}
dataframe1 = pd.DataFrame(data1)
dataframe1.set_index('CI Config Admin Group', inplace=True)

data2 = {
    "CI Config Admin Group": ["team2", "team1", "team1"],
    "column3": ["value5", "value6", "value7"]
}
dataframe2 = pd.DataFrame(data2)
dataframe2.set_index('CI Config Admin Group', inplace=True)

# Sample filtered reports for testing
team1_data_file1 = {
    "column1": ["value1", "value1"],
    "column2": [10, 30]
}
team1_report_file1 = pd.DataFrame(team1_data_file1, index=["team1", "team1"])

team1_data_file2 = {
    "column1": ["value1", "value1"],
    "column2": [15, 25]
}
team1_report_file2 = pd.DataFrame(team1_data_file2, index=["team1", "team1"])

team2_data_file1 = {
    "column1": ["value2"],
    "column2": [20]
}
team2_report_file1 = pd.DataFrame(team2_data_file1, index=["team2"])

team2_data_file2 = {
    "column1": ["value3"],
    "column2": [5]
}
team2_report_file2 = pd.DataFrame(team2_data_file2, index=["team2"])


if __name__ == '__main__':
    unittest.main()
