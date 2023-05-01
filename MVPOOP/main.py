import os
import data_filterer as df
import json
import file_reader as fr
import team as t
import email_generator as eg

if __name__ == "__main__":
    reader = fr.FileReader('../Reports/')
    data_tuples = reader.get_excels()

    relative_path_json = '../Reports/configuration.json'
    relative_path_template = '../Reports/template.txt'
    # # Get the absolute path of the JSON file by joining the relative path with the current file's directory

    absolute_path_json = os.path.join(os.path.dirname(__file__), relative_path_json)
    absolute_path_template = os.path.join(os.path.dirname(__file__), relative_path_template)

    with open(absolute_path_json) as f:
        config = json.load(f)
    filterer = df.DataFilterer(config, data_tuples)
    filterer.get_filters()
    filterer.loop_over()

    teams = []
    for index, row in filterer.merged_table.iterrows():
        team = t.Team(config['teams'][row[0]]['email_list'], row)
        teams.append(team)
        team.add_to_history(row)

    email_gen = eg.EmailGenerator(absolute_path_template, teams)
    email_string = email_gen.generate_emails_string()

    email_string_path = "emailStringTest.txt"  # shared folder
    f = open(email_string_path, "w")
    f.write(email_string)
    f.close()
