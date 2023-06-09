import os
import json
from data_handling import data_handler as dh
from pipeline_module.output_generation import output_generator as og


class Pipeline:

    def __init__(self, paths_file):
        self.paths_file = paths_file
        self.data_handler = None
        self.teams = None
        self.config = None
        self.local = self.paths_file['local']
        self.input_path = self.local
        self.templates_path = self.local
        self.hist_data_path = self.local
        self.string_path = ""
        self.graph_path = ""

    def get_paths(self):
        with open(self.local + self.paths_file['config']) as f:
            self.config = json.load(f)
        self.input_path += self.paths_file['input']
        template_paths = []
        for template in self.paths_file['templates']:
            path = self.local + template
            template_paths.append(path)
        self.templates_path = template_paths
        self.hist_data_path += self.paths_file['historical']
        self.string_path += self.paths_file['string']
        self.graph_path += self.paths_file['graph']

    def process_data(self):
        self.data_handler = dh.DataHandler(self.input_path, self.config, self.hist_data_path)
        self.data_handler.handle_data()
        self.teams = self.data_handler.generate_teams()

    def generate_output(self):
        output_generator = og.OutputGenerator(self.config, self.teams)
        output_generator.generate_string_output(self.templates_path, self.data_handler.pivot_tables, self.string_path)
        output_generator.generate_graph_output(self.graph_path)

    def remove_files(self):
        # Get a list of all files in the folder
        files = os.listdir(self.input_path)

        # Iterate over the files and remove them one by one
        for file in files:
            file_path = os.path.join(self.input_path, file)
            os.remove(file_path)
