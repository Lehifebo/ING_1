import file_Reader as fr
import convert_To_Pivot as ctv
import merge_Tables as mt
import pandas as pd
import convert_Groups as cg

files,path = fr.getExcels()
tables=cg.applyDictionary(ctv.toPivotTable(files,path))
merged_table = pd.merge(tables[0], tables[1], on='CI Config Admin Group', how='outer')
merged_table.fillna(0, inplace=True)
print('\n')
print(merged_table.to_string())