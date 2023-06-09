import pandas as pd
import logging
import unittest
from unittest.mock import patch
from pipeline_module.data_handling.file_reader import FileReader


# Define the unit test class
class TestFileReader(unittest.TestCase):

    def setUp(self):
        # Set up the file reader instance with the specified path
        self.file_reader = FileReader("D:/GitHub/SoftEng/SoftEng/testing/test_files/")

    def test_get_excels_with_existing_path(self):
        # Test the 'get_excels' method when the path exists
        expected_result = [
            ('file1.xlsx', pd.DataFrame()),
            ('file2.xlsx', pd.DataFrame())
        ]

        # Patch the necessary functions and mock the return values
        with patch('os.path.exists', return_value=True):
            with patch('os.listdir', return_value=['file1.xlsx', 'file2.xlsx']):
                with patch('pandas.read_excel', return_value=pd.DataFrame()):
                    result = self.file_reader.get_excels()

        # Check if the expected files and dataframes are found in the result
        for expected_file, expected_df in expected_result:
            found = False
            for result_file, result_df in result:
                if expected_file == result_file and expected_df.equals(result_df):
                    found = True
                    break
            self.assertTrue(found)

    def test_get_excels_with_nonexistent_path(self):
        # Test the 'get_excels' method when the path does not exist
        with patch('os.path.exists', return_value=False), \
                self.assertLogs(level=logging.WARNING) as cm:
            self.file_reader.get_excels()

        # Check if the warning message is logged correctly
        self.assertIn(f"Path {self.file_reader.path} does not exist.", cm.output[0])

    def test_get_excels_with_invalid_file_extension(self):
        # Test the 'get_excels' method when the path contains files with invalid extensions
        expected_result = [('file1.xlsx', pd.DataFrame())]

        # Patch the necessary functions and mock the return values
        with patch('os.path.exists', return_value=True):
            with patch('os.listdir', return_value=['file1.xlsx', 'dummy.txt']):
                with patch('pandas.read_excel', return_value=pd.DataFrame()):
                    result = self.file_reader.get_excels()

        # Check if the expected file and dataframe are found in the result
        self.assertEqual(len(result), len(expected_result))
        for (expected_file, expected_df), (result_file, result_df) in zip(expected_result, result):
            self.assertEqual(expected_file, result_file)
            self.assertTrue(expected_df.equals(result_df))
