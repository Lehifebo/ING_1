import unittest
from unittest.mock import MagicMock
from pipeline_module.data_handling.data_handler import DataHandler


class TestDataHandler(unittest.TestCase):
    def setUp(self):
        self.config = {
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


if __name__ == '__main__':
    unittest.main()
