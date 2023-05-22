import graph_generator as gg
import string_generator as sg


class OutputGenerator:
    def __init__(self, config, teams, template_paths, data, string_path, hist_data_path):
        self.config = config
        self.teams = teams
        self.template_paths = template_paths
        self.data = data
        self.string_path = string_path
        self.hist_data_path = hist_data_path

    def generate_output(self):
        tribe_lead_email = self.config['tribe_lead']  # should be in try catch
        string_generator = sg.StringGenerator(self.template_paths, self.teams, tribe_lead_email, self.data)
        string = string_generator.generate_output_string()
        string_generator.create_string_file(self.string_path, string)

        graph_generator = gg.GraphGenerator(self.teams)
        graph_generator.create_team_graphs(self.hist_data_path)
