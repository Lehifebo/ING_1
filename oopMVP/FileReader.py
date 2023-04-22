import os


class FileReader:
    def __init__(self, path):
        self.path = path

    def getExcels(self):
        # Get the current directory
        path = self.path  # os.path.dirname(__file__)
        files = []
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                if "xlsx" in file_name:
                    files.append(file_name)
        return files, (path + '\\')
