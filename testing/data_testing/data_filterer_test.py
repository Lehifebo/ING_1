import unittest
import pandas as pd
from pipeline_module.data_handling.data_filterer import DataFilterer


# Define the unit test class
class TestDataFilterer(unittest.TestCase):
    def setUp(self):
        # Set up the necessary configurations and data tuples for the test
        self.config = {
            # Configuration for file1
            "filenames": ["file1", "file2"],
            "file1": {
                "filters": {
                    "column1": "value1",
                    "column3": "value3"
                },
                "rows": ["column1"],
                "values": {
                    "column2": {
                        "aggfunc": "sum",
                        "fill_value": 0
                    }
                }
            },
            # Configuration for file2
            "file2": {
                "filters": {
                    "column1": "value3"
                },
                "rows": ["column1"],
                "values": {
                    "column2": {
                        "aggfunc": "mean",
                        "fill_value": 0
                    }
                }
            },
            # Team configurations
            "teams": {
                "team1": {
                    "aliases": ["alias1", "alias2"]
                },
                "team2": {
                    "aliases": ["alias3"]
                }
            },
            "aggregateColumn": "team"
        }

        # Sample data tuples for testing
        self.data_tuples = [
            ("file1", pd.DataFrame({"column1": ["value1", "value2", "value3"], "column2": [1, 2, 3]})),
            ("file2", pd.DataFrame({"column1": ["value3", "value4", "value5"], "column2": [4, 5, 6]}))
        ]

    def test_get_filters(self):
        # Test the 'get_filters' method
        data_filterer = DataFilterer(self.config, self.data_tuples)
        filters = data_filterer.get_filters()
        expected_filters = {
            "file1": {
                "column1": "value1",
                "column3": "value3"
            },
            "file2": {
                "column1": "value3"
            }
        }
        self.assertEqual(filters, expected_filters)

    def test_map_team_names(self):
        # Test the 'map_team_names' method
        data_filterer = DataFilterer(self.config, self.data_tuples)
        current_tuple = ("file1", pd.DataFrame({"team": ["alias2", "alias3", "alias1"]}))

        data_filterer.map_team_names(current_tuple)

        expected_result = pd.DataFrame({"team": ["team1", "team2", "team1"]})
        pd.testing.assert_frame_equal(current_tuple[1], expected_result)

    def test_get_mapping(self):
        # Test the 'get_mapping' method
        data_filterer = DataFilterer(self.config, self.data_tuples)
        team_name = "alias1"
        mapping = data_filterer.get_mapping(team_name)
        self.assertEqual(mapping, "team1")

    def test_filter_data(self):
        # Test the 'filter_data' method
        data_filterer = DataFilterer(self.config, self.data_tuples)
        current_tuple = ("file1", pd.DataFrame({"column1": ["value1", "value1", "value2"], "column2": [1, 2, 3],
                                                "column3": ["value3", "value2", "value3"]}))

        expected_filters = {
            "file1": {
                "column1": "value1",
                "column3": "value3"
            },
            "file2": {
                "column1": "value3"
            }
        }
        data_filterer.filters = expected_filters

        filtered_data = data_filterer.filter_data(current_tuple)

        expected_result = pd.DataFrame({"column1": ["value1"], "column2": [1],
                                        "column3": ["value3"]})
        pd.testing.assert_frame_equal(filtered_data, expected_result)

    def test_convert_to_pivot(self):
        # Test the 'convert_to_pivot' method
        data_filterer = DataFilterer(self.config, self.data_tuples)
        filtered_data = pd.DataFrame({"column1": ["value1", "value2"], "column2": [5, 7]})
        filename = "file2"

        pivot_table = data_filterer.convert_to_pivot(filtered_data, filename)

        expected_pivot_table = ("file2", pd.DataFrame({"column2": [5, 7, 6]}, index=["value1", "value2", "All"]))
        expected_pivot_table = expected_pivot_table[1].values
        pivot_table = pivot_table[1].values
        self.assertEqual(pivot_table.all(), expected_pivot_table.all())

    def test_return_pivot(self):
        # Test the 'return_pivot' method
        data_filterer = DataFilterer(self.config, self.data_tuples)
        filtered_data = pd.DataFrame({"column1": ["value1", "value2"], "column2": [5, 7]})
        index_columns = ["column1"]
        values_columns = ["column2"]
        aggfuncs = {'column2': "sum"}
        fill_values = {"column2": 0}
        filename = "file1"

        pivot_table = data_filterer.return_pivot(aggfuncs, fill_values, filtered_data, index_columns, values_columns,
                                                 filename)

        expected_pivot_table = pd.DataFrame({"column2": [5, 7, 12]}, index=["value1", "value2", "All"])
        expected_pivot_table = expected_pivot_table.values
        pivot_table = pivot_table.values
        self.assertEqual(pivot_table.all(), expected_pivot_table.all())


if __name__ == '__main__':
    unittest.main()
