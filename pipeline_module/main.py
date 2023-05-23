import json
import pipeline as pl

if __name__ == "__main__":
    paths_path = "paths.json"
    with open(paths_path) as f:
        paths = json.load(f)
    pipeline = pl.Pipeline(paths)
    pipeline.get_paths()
    pipeline.process_data()  # data stuff
    pipeline.generate_output()  # output stuff
    # pipeline.remove_files()
