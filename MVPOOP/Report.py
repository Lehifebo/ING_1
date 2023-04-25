

class Report:
    def __init__(self, team, team_data, date):
        self.team = team
        self.vulnerabilities = None #get from team data
        self.overdue_vulnerabilities = None
        self.compliances = None
        self.date= date