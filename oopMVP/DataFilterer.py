import pandas as pd


class DataFilterer:
    def __init__(self, path, config, df):
        self.path = path #specify path of what or itll get confuding
        self.config = config
        self.df = df  # maybe file instead
        self.merged_table = None
        self.tables = None

    def map_team_names(self):
        try:
            self.df['CI Config Admin Group'] = self.df['CI Config Admin Group'].apply(self.get_mapping)
        except ValueError as e:
            print(e)
            exit(0)
    def get_mapping(self,team_name):
        team_mapping = self.config['teams']
        for team, names in team_mapping.items(): #search in each array  for the desired team names
            if team_name in names:
                return team #if the name is found, return the mapping
        raise ValueError("Team '" +team_name + "' has no mapping")
    
