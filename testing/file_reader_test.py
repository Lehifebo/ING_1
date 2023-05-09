import os
import pandas as pd
import unittest
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.file_reader import FileReader


class TestFileReader(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.dirname(__file__)

    def test_non_existent_path(self):
        with self.assertRaises(ValueError):
            file_reader = FileReader('non_existent_path')
            file_reader.get_excels()

    def test_get_excels(self):
        file_reader = FileReader(self.test_dir)
        dataframes = file_reader.get_excels()

        self.assertEqual(len(dataframes), 2)

        expected_dataframes = [
            ('file1.xlsx', pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})),
            ('file2.xlsx', pd.DataFrame({'col1': [5, 7], 'col2': [6, 8]}))
        ]

        for i, (name, df) in enumerate(expected_dataframes):
            self.assertEqual(name, dataframes[i][0])
            pd.testing.assert_frame_equal(df, dataframes[i][1])


if __name__ == '__main__':
    unittest.main()