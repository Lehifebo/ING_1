import os
import DataFilterer as dataFilter
import json
import FileReader as fr
import Team
import EmailGenerator
reader = fr.FileReader('Reports')
data_tuples=reader.getExcels()

relative_path_json = '../Reports/configuration.json'
relative_path_template = '../Reports/template.txt' 
# # Get the absolute path of the JSON file by joining the relative path with the current file's directory

absolute_path_json = os.path.join(os.path.dirname(__file__), relative_path_json)
absolute_path_template = os.path.join(os.path.dirname(__file__), relative_path_template)

with open(absolute_path_json) as f:
            config = json.load(f)
filterer = dataFilter.DataFilterer(config,data_tuples)
filterer.get_filters()

filterer.loop_over()

teams=[]
for index, row in filterer.merged_table.iterrows(): 
    team = Team.Team(config['teams'][row[0]]['email_list'],row)
    teams.append(team)

email_generator= EmailGenerator.EmailGenerator(absolute_path_template,teams)
email_string = email_generator.generate_emails_string()

email_string_path = "emailStringTest.txt" #shared folder
f = open(email_string_path, "w")
f.write(email_string)
f.close()