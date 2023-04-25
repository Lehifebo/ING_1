import os
import pandas as pd

class FileReader:
    def __init__(self, path):
        self.path = path

    def getExcels(self):
        # Get the current directory
        path = self.path  # os.path.dirname(__file__)
        dataframes = []
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                if "xlsx" in file_name:
                    df = pd.read_excel(self.path+'/'+file_name)
                    dataframes.append((file_name.split('_')[0],df))
        return dataframes
