import pandas as pd
import parse_Config as pc

def toPivotTable(files):
    tables=[]
    for file in files:
        # Read Excel file into a pandas DataFrame
        excel = pd.read_excel(file)
        # get the pivot table settings
        (filtersFile,valuesFile,indexFile,aggfuncFile) = pc.pivotTabelSettings(file.split('_')[0]+"_config")
        #filter the data
        excel_filtered = excel.query(filtersFile)
        #create the pivot table
        pivot_table = pd.pivot_table(excel_filtered, values=valuesFile, index=indexFile, aggfunc=aggfuncFile)
        tables.append(pivot_table)
    return tables