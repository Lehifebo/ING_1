import os
import json
def generateEmails(table):
    splitInEmail="\n\nsplitInEmail\n\n"
    splitBEmails="\nsplitBetweenEmails\n"
    finalMail=''
    path = os.path.dirname(__file__) #get the absolute path of the file

    template=readTemplate(path+"\\template.txt") #get the template string
    allEmails=readEmails((path+"\\emailingList.txt"))

    for index,row in table.iterrows():
        pairs=zip(table.columns,row.values) #match the value with the header
        formatting=[]
        teamName=next(pairs)[1]
        if teamName in allEmails:#if the header is in the email listing 
            formatting.append(teamName) #get the group name witouth the header
            for pair in pairs:
                teamEmails = allEmails[teamName]
                if(pair[1]!=0): #if the team has non-zero value
                    formatting.append(pair[0])
                    formatting.append(pair[1])
                else:
                    formatting.append("no issues with")
                    formatting.append(pair[0])        
            finalMail+=splitBEmails
            finalMail+=(','.join(teamEmails))
            finalMail+=splitInEmail
            finalMail+=template.format(*formatting) ## add the email to the final list
        else:
            finalMail.append("Team emails not found.")

    return finalMail

def readTemplate(path):
    with open(path, 'r') as file:
        return file.read()
    
def readEmails(path):
    with open(path, 'r') as file:
        return json.loads(file.read())
    