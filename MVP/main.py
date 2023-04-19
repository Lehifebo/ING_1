import file_Reader as fr
import convert_To_Pivot as ctv
import map_Groups as mg
import merge_Tables as mt
import generateEmails as ge
files, path = fr.getExcels()
tables = mg.applyDictionary(ctv.toPivotTable(files, path))
merged_table = mt.merge(tables,'CI Config Admin Group')
merged_table.fillna(0, inplace=True)
#print(merged_table)
#print(ge.generateEmails(merged_table))
path = "emailString.txt" #can be changed to another folder
f = open(path, "w")
f.write(ge.generateEmails(merged_table))
f.close()

