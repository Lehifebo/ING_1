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

    relative_path_json = '../configurations/configuration.json'
    relative_path_template = '../configurations/template.txt'
    relative_path_template_tribe_lead = '../configurations/tribeLeadTemplate.txt'

    # # Get the absolute path of the JSON file by joining the relative path with the current file's directory

    absolute_path_json = os.path.join(
        os.path.dirname(__file__), relative_path_json)
    absolute_path_template = os.path.join(
        os.path.dirname(__file__), relative_path_template)
    absolute_path_template_tribe_lead = os.path.join(
        os.path.dirname(__file__), relative_path_template_tribe_lead)

    with open(absolute_path_json) as f:
        config = json.load(f)
    filterer = df.DataFilterer(config, data_tuples)
    filterer.loop_over()

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

    email_gen = eg.EmailGenerator(absolute_path_template, absolute_path_template_tribe_lead, teams)
    email_string = email_gen.generate_emails_string()
    try:
        email_string += email_gen.overview_email(config['tribe_lead'], filterer.merged_table)
        email_string_path = os.path.join(project_dir, "output/text/emailStringTest.txt") #shared folder
        f = open(email_string_path, "w")
        f.write(email_string)
        f.close()
    except KeyError as e:
        logging.warning(f"{e} is not set.")
        exit(0)
    graph_gen = gg.GraphGenerator(teams)
    graph_gen.create_team_graphs()
