from .graph_generator import GraphGenerator
from .string_generator import StringGenerator


class OutputGenerator:
    def __init__(self, config, teams):
        self.config = config
        self.teams = teams

    def generate_string_output(self, template_paths, data, string_path):
        tribe_lead_email = self.config['tribe_lead']  # should be in try catch
        string_generator = StringGenerator(template_paths, self.teams, tribe_lead_email, data)
        string = string_generator.generate_output_string()
        string_generator.create_string_file(string_path, string)

    def generate_graph_output(self, hist_data_path):
        # will config need to be used here? else move config to other function
        graph_generator = GraphGenerator(self.teams)
        graph_generator.create_team_graphs(hist_data_path)
        # probs create tribe lead graph somehow
