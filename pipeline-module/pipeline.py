from data_handling import data_handler as dh
from output_generation import output_generator as og


class Pipeline:

    def __init__(self, paths_file):
        self.paths_file = paths_file
        self.data_handler = None
        self.config = None
        self.input_path = None
        self.templates_path = None
        self.hist_data_path = None
        self.string_path = None
        self.graph_path = None
        self.teams = None

    def get_paths(self):
        # get all the files/paths and set the fields
        print("hello")

    def start_pipeline(self):
        self.data_handler = dh.DataHandler(self.input_path, self.config)
        self.data_handler.handle_data()
        self.teams = self.data_handler.generate_teams()

    def end_pipeline(self):
        output_generator = og.OutputGenerator(self.config, self.teams)
        output_generator.generate_string_output(self.templates_path, self.data_handler.data, self.string_path)
        output_generator.generate_graph_output(self.hist_data_path)
