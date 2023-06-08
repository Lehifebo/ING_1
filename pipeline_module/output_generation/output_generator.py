from .graph_generator import GraphGenerator
from .string_generator import StringGenerator


class OutputGenerator:
    def __init__(self, config, teams):
        self.config = config
        self.teams = teams

    def generate_string_output(self, template_paths, data_tuples, string_path):
        tribe_lead_email = self.config['tribe_lead']
        string_generator = StringGenerator(template_paths, self.teams, tribe_lead_email, data_tuples)
        string = string_generator.generate_output_string()
        string_generator.create_string_file(string_path, string)

    def generate_graph_output(self, graph_path):
        graph_generator = GraphGenerator(self.teams, graph_path)
        graph_generator.create_team_graphs()
        graph_generator.create_tribe_lead_graphs(self.config["issue_columns"])
