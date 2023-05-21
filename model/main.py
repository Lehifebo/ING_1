import os
import data_filterer as df
import json
import file_reader as fr
import team as t
import email_generator as eg
import logging
import graph_generator as gg

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get the path to the Reports directory relative to the MVPOOP directory
reports_dir = os.path.join(project_dir, "excel_data")

if __name__ == "__main__":
    reader = fr.FileReader(reports_dir)
    data_tuples = reader.get_excels()

    rel_path_json = '../configurations/configuration.json'
    rel_path_template = '../configurations/template.txt'
    rel_path_template_tribe_lead = '../configurations/tribeLeadTemplate.txt'

    # # Get the absolute path of the JSON file by joining the relative path with the current file's directory

    abs_path_json = os.path.join(
        os.path.dirname(__file__), rel_path_json)
    abs_path_template = os.path.join(
        os.path.dirname(__file__), rel_path_template)
    abs_path_template_tribe_lead = os.path.join(
        os.path.dirname(__file__), rel_path_template_tribe_lead)

    with open(abs_path_json) as f:
        config = json.load(f)
    filterer = df.DataFilterer(config, data_tuples)
    filterer.filter_files()

    teams = []
    team_dict = config['teams']
    team_names = list(team_dict.keys())
    for index, row in filterer.merged_table.iterrows():
        try:
            team = t.Team(team_dict[row[0]]['email_list'], row, team_names[index])
            teams.append(team)
            team.add_to_history(row)
        except KeyError as e:
            logging.error(f"{e} is missing for team {team_names[index]}")
            exit(0)

    try:
        tribe_lead_email = config['tribe_lead']
        email_gen = eg.EmailGenerator(abs_path_template, abs_path_template_tribe_lead, teams,
                                      tribe_lead_email, filterer.merged_table)
        email_string = email_gen.generate_output_string()
        email_string_path = os.path.join(project_dir, "output/text/emailStringTest.txt")  # shared folder
        email_gen.create_string_file(email_string_path, email_string)
    except KeyError as e:
        logging.warning(f"tribe_lead is not set.")
        exit(0)

    graph_gen = gg.GraphGenerator(teams)
    graph_gen.create_team_graphs()
