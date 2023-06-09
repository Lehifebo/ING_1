import os
import pandas as pd
import logging


class FileReader:
    def __init__(self, path):
        # Initialize the FileReader object with a given path
        self.path = path

    def get_excels(self):
        # Get the Excel files from the specified directory
        path = self.path

        # Check if the path exists
        if not os.path.exists(path):
            logging.warning(f"Path {path} does not exist.")

        dataframes = []

        # Iterate over the files in the directory
        for file_name in os.listdir(path):
            # Check if the file is a valid Excel file
            if os.path.isfile(path + file_name) and "xlsx" in file_name:
                # Read the Excel file into a pandas DataFrame
                df = pd.read_excel(path + file_name)

                # Assume that the file names are matching XXXX_
                dataframes.append((file_name.split('_')[0], df))

        return dataframes
