import json
import os


class EmailGenerator:
    def __init__(self, template_path, team_list):
        self.team_list = team_list
        self.template_path = template_path

    def generateEmails(self,table):
        splitInEmail = "\n\nsplitInEmail\n\n"
        splitBEmails = "\nsplitBetweenEmails\n"
        finalMail = ''
        path = os.path.dirname(__file__)  # get the absolute path of the file

        template = self.readTemplate(path + "\\template.txt")  # get the template string
        allEmails = self.readEmails((path + "\\emailingList.txt"))

        for index, row in table.iterrows():
            pairs = zip(table.columns, row.values)  # match the value with the header
            formatting = []
            teamName = next(pairs)[1]
            if teamName in allEmails:  # if the header is in the email listing
                formatting.append(teamName)  # get the group name witouth the header
                for pair in pairs:
                    teamEmails = allEmails[teamName]
                    formatting.append(pair[0])
                    formatting.append(pair[1])
                if index != 0:
                    finalMail += splitBEmails
                finalMail += (','.join(teamEmails))
                finalMail += splitInEmail
                finalMail += template.format(*formatting)  ## add the email to the final list
            else:
                finalMail.append("Team emails not found.")

        return finalMail

    def readTemplate(self,path):
        with open(path, 'r') as file:
            return file.read()

    def readEmails(self,path):
        with open(path, 'r') as file:
            return json.loads(file.read())