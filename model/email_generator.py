import json
import logging
import os


def read_template(path):
    with open(path, 'r') as file:
        return file.read()


class EmailGenerator:
    def __init__(self, template_path, team_list):
        self.team_list = team_list
        self.template = read_template(template_path)
        self.splitInEmail = "\n\nsplitInEmail\n\n"
        self.split_between_mails = "\nsplitBetweenEmails\n"

    def generate_email(self, team):
        email = ''
        email += self.add_email_list(team)
        email += self.fill_template(team)
        return email

    def add_email_list(self, team):
        email_list = ''
        for item in team.emailing_list:
            email_list += item + ","
        email_list = email_list[:-1]
        email_list += self.splitInEmail
        return email_list

    def fill_template(self, team):
        data = []
        # match the value with the header
        pairs = zip(team.report.index, team.report.values)
        data.append(next(pairs)[1])  # skip the name
        for pair in pairs:
            data.append(pair[0])  # header
            data.append(pair[1])  # value
        return self.template.format(*data)

    def generate_emails_string(self):
        final_mail = ''
        try:
            for team in self.team_list:
                team_email = self.generate_email(team)
                final_mail += team_email
                final_mail += self.split_between_mails
        except KeyError as e:
            logging.error('You have more/less {} than columns in table')
            exit(0)
        # remove the final splitBetweenEmails
        final_mail = final_mail.rstrip(self.split_between_mails)
        return final_mail

    def overview_email(self, email, overview):
        string = ''
        string += self.split_between_mails
        string += email
        string += self.splitInEmail
        string += "Here is an overview of the teams \n"
        string += overview.to_string(index=False)
        string +="\n Best Regards, \n Name"
        return string
