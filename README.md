# SoftEng
# User's Manual

## Description
This program is the first of two parts of a system that analyses Excel data files and sends reports about them to the teams involved.
This Python application uses instructions to set up in the “configurations.json” file to filter all the Excel files in the input folder and create pivot tables summarising the data in them.
It then splits and aggregates the pivot tables based on the teams in order to generate graphs and reports for both the team members and the tribe lead. 
Below are the instructions for any user who wishes to use the application.

## Excel Data files:
* These are the conditions the Excel files need to have in order for the program to work:
* The Excel files need to be in the input folder defined in the file paths.json.
* The Excel files need be in .xlsx format.
* The Excel files need to have an underscore “_” in the name.
* The Excel files need to contain only 1 sheet.
* The Excel files need to share one column that can be used to group the data after the filtering.
* The settings to filter the Excel files and create a pivot table need to be defined in the configuration.json file.

## configuration.json:
This files defines how the Excel files should be filtered and holds the information regarding the teams and the tribe leads. Here is an explanation of every field:
* “aggregateColumn”: the column that is shared between all the files and that contains the team names.
* “filenames”: a list of names of every file before the underscore. For each of these names a dictionary needs to be set up containing the following keys: “filters”, “rows”, “columns” and “values”.
* “filters”: a dictionary containing the filters for the file. The dictionary needs to contain the column as the key and the value desired as the value.
* “rows”: list of columns from the file that should be used as rows in the pivot table.
* “columns”: list of columns from the file that should be used as columns in the pivot table.
* “values”: a dictionary containing a dictionary for every value that should be in the pivot table. For each value, the “aggfunc” and the “fill_value” need to be defined.
* “aggfunc”: what function to apply on the value for the pivot table, needs to be one of the options from Excel pivot tables.
* “fill_value”: a boolean (1 or 0) to define whether to fill the empty values or leave them empty.
* “teams”: a dictionary containing a dictionary for every team. The JSON field defining the team dictionary should be named with the desired display name for the final report. For each team there are the fields “aliases” and “email_list”.
* “aliases”: a list of all the different names the same team has in the aggregate column.
* “email_list”: a list of the email addresses of all the members of the team.
* “tribe_lead”: the email address of the tribe lead.
* “issue_columns”: The issues that the tribe lead will receive a graph on. Need to match the “values” keys.

## template.txt and tribeLeadTemplate.txt:
The template.txt and tribeLeadTemplate.txt files can be used to define the content of the emails for the teams and for the tribe lead respectively.
It can be changed before running the program in order to add announcements etc.
Every set of brackets “{}” is filled with data. The first set is filled with the team name while the others are with file names and issues for said files. 
If a new file needs to get processed two sets of brackets also need to be added.

## paths.json:
The paths.json file is used to define the paths to all the necessary folders and files.
As the user, the only thing necessary is to set “local” to the absolute path of the main project folder.

## Running the application:
1. Add the Excel data files to the input folder.
2. Open the IDE of your choice.
3. Check that the settings for filters and that the templates are as desired.
4. Click on the play button (green triangle) at the top.

## Power Automate:
In order to connect the Python Application to Power Automate for email sending two steps are necessary:
Synchronise the output folder between the local machine to Microsoft Sharepoint.
Copy the path of the Sharepoint folder and set it as the folder the Power Automate flow should scan for its triggering.