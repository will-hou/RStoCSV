import argparse
import json
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help="the path to the JSON file you want to convert", type=str)
args = parser.parse_args()

with open(args.path) as file_path:
    json_data = json.load(file_path)

# The total number of scouted metrics
num_metrics = len(json_data['teams'][list(json_data['teams'].keys())[0]][0]['metrics'])

# Find total number of scouts
num_scouts = 0

for i in json_data['teams'].values():
    num_scouts += len(i)

# Preallocate numpy array with number of scouts and the number of metrics
data = np.zeros((num_scouts, num_metrics), dtype='O')

# List of all metrics scouted for
headers = [i['name'] for i in json_data['teams'][list(json_data['teams'].keys())[0]][0]['metrics'].values()]

# Put scout data into a numpy array
y_pos = 0
for team in json_data['teams'].values():
    for scout in team:
        temp = [i['value'] for i in scout['metrics'].values()]
        data[y_pos] = temp
        y_pos += 1

# Put scout names into numpy array
scout_names = []
for team in json_data['teams'].values():
    for scout in team:
        scout_names.append(scout['name'])
scout_names = np.vstack(np.asarray(scout_names))
data = np.concatenate((scout_names, data), axis=1)

# Put team numbers into numpy array
team_nums = []
for team in json_data["teams"]:
    for i in range(0, len(json_data["teams"][team])):
        team_nums.append(team)
team_nums = np.vstack(np.asarray(team_nums))
data = np.concatenate((team_nums, data), axis=1)

print(data.shape)
# Add team number and name of scout to the CSV header
headers.insert(0, "Name of Scout")
headers.insert(0, "Team Number")

# Convert array into dataframe
table = pd.DataFrame(data=data, columns=headers)
# Save data frame as an html file
table.to_html("frame.html")
# Convert data frame to csv
table.to_csv("scout.csv", index=False)
