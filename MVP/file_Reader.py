import os

def getExcels():
    # Get the current directory
    path = os.path.dirname(__file__)
    files=[]
    for file_name in os.listdir(path):
        if os.path.isfile(os.path.join(path, file_name)):
            if "xlsx" in file_name:
                files.append(file_name)
    return files,(path+'\\')

