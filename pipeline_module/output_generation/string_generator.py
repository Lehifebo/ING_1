import json
import logging
import os


def read_template(path):
    with open(path, 'r') as file:
        return file.read()


class StringGenerator:
    def __init__(self, template_paths, team_list, tribe_lead_email, overview):
        self.team_list = team_list
        self.template = read_template(template_paths[0])
        self.tribe_lead_template = read_template(template_paths[1])
        self.splitInEmail = "\n\nsplitInEmail\n\n"
        self.split_between_mails = "\nsplitBetweenEmails\n"
        self.tribe_lead_email = tribe_lead_email
        self.overview = overview

    def generate_output_string(self):
        final_string = self.generate_teams_string()

        #final_string += self.generate_overview_email()
        return final_string

    def generate_teams_string(self):
        final_mail = ''
        try:
            for team in self.team_list:
                team_email = self.generate_team_email(team)
                final_mail += team_email
                final_mail += self.split_between_mails
        except KeyError as e:
            logging.error('You have more/less {} than columns in table')
            exit(0)
        # remove the final splitBetweenEmails
        final_mail = final_mail.rstrip(self.split_between_mails)
        return final_mail

    def generate_team_email(self, team):
        email = ''
        email += self.add_email_list(team)
        email += self.fill_team_template(team)
        return email

    def add_email_list(self, team):
        email_list = ''
        for item in team.emailing_list:
            email_list += item + ","
        email_list = email_list[:-1]
        email_list += self.splitInEmail
        return email_list

    def fill_team_template(self, team):
        data = []
        data.append(team.team_name)
        for (file, report) in team.report:
            data.append(file)
            data.append(report.to_string())
        # # match the value with the header
        # pairs = zip(team.report.index, team.report.values)
        # data.append(next(pairs)[1])  # skip the name
        # for pair in pairs:
        #     data.append(pair[0])  # header
        #     data.append(pair[1])  # value
        return self.template.format(*data)

    def generate_overview_email(self):
        string = ''
        string += self.split_between_mails
        string += self.tribe_lead_email
        string += self.splitInEmail
        to_string = self.overview.to_string(index=False)
        print(to_string)
        try:
            string += self.tribe_lead_template.format(to_string)
        except IndexError:
            logging.error("The number of {} is greater than 1.")
            exit(0)
        return string

    def create_string_file(self, path, string):
        f = open(path, "w")
        f.write(string)
        f.close()
