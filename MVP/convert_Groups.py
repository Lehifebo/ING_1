import os
import file_Reader as fr
import convert_To_Pivot as ctv
import merge_Tables as mt
import pandas as pd

def applyDictionary(tables):
    path = os.path.dirname(__file__) #get the absolute path of the file
    conversion_dict=createDictionary(path+"\\conversionSheet.txt") #get the conversion sheet
    newTables=[]
    for table in tables:
        newTables.append(table.rename(index=conversion_dict)) #apply the dictionary
    return newTables

def createDictionary(path):
    with open(path, 'r') as file:
        conversion_dict = {}
        for line in file:
            key, value = line.strip().split()
            conversion_dict[value] = key
    return conversion_dict

