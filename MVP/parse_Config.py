import re
def pivotTabelSettings(config):
    with open(config, 'r') as file:#open the file for reading
        filters=parseFilters(file)
        (values,index,aggfunc)=parseHeader(file)
    return (filters,values,index,aggfunc)

def parseFilters(file):
    doneFilters = False
    filters=''
    currentLine = file.readline()
    currentLine=currentLine.rstrip(' \t\n') #remove trailing characters
    #this part will cycle trough the filter lines
    while(currentLine!='' and doneFilters == False):
        rowName = '`' + currentLine.split('\t')[0] + '`'
        attribute = currentLine.split('\t')[1]
        if ("false" in attribute):
            value = attribute.capitalize()
        else:
            value = f"'{attribute}'"
        filters += f"{rowName} == {value} & "
        currentLine = file.readline()
        currentLine=currentLine.rstrip(' \t\n') #remove trailing characters
    doneFilters = True
    return filters[:-2]

def parseHeader(file):
    currentLine = file.readline()
    currentLine=currentLine.rstrip(' \t\n') #remove trailing characters
    currentLine=currentLine.split('\t')
    size=len(currentLine)
    iter=0
    index=[]
    values=[]
    aggfunc=currentLine[size-1].split(' ')[0].lower() #take the function from the last header as aggregate function

    #I assume the header will be "function of value"
    #get the indexes
    while(iter<size and currentLine[iter].split(' ')[0]!=aggfunc.capitalize()): #iterate while there are elements left, and there is not a counting function
        index.append(currentLine[iter])
        iter+=1

    #get the values
    while(iter<size):
        values.append(' '.join(currentLine[iter].split(' ')[2:])) # the 2 will skip over the "function of" part
        iter+=1

    
    return values,index,aggfunc