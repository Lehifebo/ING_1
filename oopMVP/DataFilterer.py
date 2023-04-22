import pandas as pd
import os


class DataFilterer:
    def __init__(self, path, config, df):
        self.path = path #specify path of what or itll get confuding
        self.config = config
        self.df = df  # maybe file instead
        self.merged_table = None
        self.tables = None

    def apply_dictionary(self):
        path = os.path.dirname(__file__)  # get the absolute path of the file
        conversion_dict = self.create_dictionary(path + "\\conversionSheet.txt")  # get the conversion sheet
        newTables = []
        for table in self.tables:
            newTables.append(table.rename(index=conversion_dict))  # apply the dictionary
        return newTables

    def create_dictionary(self,path):
        with open(path, 'r') as file:
            conversion_dict = {}
            for line in file:
                key, value = line.strip().split()
                conversion_dict[value] = key
        return conversion_dict

    def to_pivot_table(self,files, path):
        tables = []
        for file in files:
            # Read Excel file into a pandas DataFrame
            excel = pd.read_excel(path + file)
            # get the pivot table settings
            (filtersFile, valuesFile, indexFile, aggfuncFile) = self.pivotTabelSettings(
                path + file.split('_')[0] + "_config")
            # filter the data
            excel_filtered = excel.query(filtersFile)
            # create the pivot table
            pivot_table = pd.pivot_table(excel_filtered, values=valuesFile, index=indexFile, aggfunc=aggfuncFile)
            tables.append(pivot_table)
        return tables

    def pivotTabelSettings(self,config):
        with open(config, 'r') as file:  # open the file for reading
            filters = self.parseFilters(file)
            (values, index, aggfunc) = self.parseHeader(file)
        return (filters, values, index, aggfunc)

    def parseFilters(self,file):
        doneFilters = False
        filters = ''
        currentLine = file.readline()
        currentLine = currentLine.rstrip(' \t\n')  # remove trailing characters
        # this part will cycle trough the filter lines
        while (currentLine != '' and doneFilters == False):
            rowName = '`' + currentLine.split('\t')[0] + '`'
            attribute = currentLine.split('\t')[1]
            if ("false" in attribute):
                value = attribute.capitalize()
            else:
                value = f"'{attribute}'"
            filters += f"{rowName} == {value} & "
            currentLine = file.readline()
            currentLine = currentLine.rstrip(' \t\n')  # remove trailing characters
        doneFilters = True
        return filters[:-2]

    def parseHeader(self,file):
        currentLine = file.readline()
        currentLine = currentLine.rstrip(' \t\n')  # remove trailing characters
        currentLine = currentLine.split('\t')
        size = len(currentLine)
        iter = 0
        index = []
        values = []
        aggfunc = currentLine[size - 1].split(' ')[
            0].lower()  # take the function from the last header as aggregate function

        # I assume the header will be "function of value"
        # get the indexes
        while (iter < size and currentLine[iter].split(' ')[
            0] != aggfunc.capitalize()):  # iterate while there are elements left, and there is not a counting function
            index.append(currentLine[iter])
            iter += 1

        # get the values
        while (iter < size):
            values.append(' '.join(currentLine[iter].split(' ')[2:]))  # the 2 will skip over the "function of" part
            iter += 1

        return values, index, aggfunc

    def merge(self,tables, collumn):
        merged_table = pd.DataFrame(columns=[collumn])
        for table in tables:
            merged_table = pd.merge(merged_table, table, on=collumn, how='outer')
        return merged_table