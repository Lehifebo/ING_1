import json
import pipeline as pl

if __name__ == "__main__":
    # Define the path to the JSON file containing paths
    paths_path = "paths.json"

    # Load the paths from the JSON file
    with open(paths_path) as f:
        paths = json.load(f)

    # Create an instance of the Pipeline class
    pipeline = pl.Pipeline(paths)

    # Get the paths from the Pipeline object
    pipeline.get_paths()

    # Process the data using the Pipeline object
    pipeline.process_data()

    # Generate the output using the Pipeline object
    pipeline.generate_output()

    # Remove unnecessary files using the Pipeline object
    pipeline.remove_files()
