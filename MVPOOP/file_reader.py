import os
import pandas as pd


class FileReader:
    def __init__(self, path):
        self.path = path

    def get_excels(self):
        # Get the current directory
        path = self.path
        if not os.path.exists(path):
            raise ValueError(f"Path {path} does not exist.")
        dataframes = []
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                if "xlsx" in file_name:
                    # read the excel files to pandas df
                    df = pd.read_excel(os.path.join(path, file_name))
                    # assume that the file names are matching XXXX_
                    dataframes.append((file_name.split('_')[0], df))
        return dataframes
