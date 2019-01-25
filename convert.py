import argparse
import json
import os

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', help="the path to the JSON file you want to convert", type=str)
args = parser.parse_args()

try:
    with open(args.path) as file_path:
        json_data = json.load(file_path)
except json.decoder.JSONDecodeError:
    print("Please use a valid Robot Scouter JSON (.json) file")
    exit()

# The total number of scouted metrics
try:
    num_metrics = len(json_data['teams'][list(json_data['teams'].keys())[0]][0]['metrics'])
except KeyError:
    print("Please use a valid Robot Scouter JSON (.json) file")
    exit()

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

# Add team number and name of scout to the CSV header
headers.insert(0, "Name of Scout")
# Convert array into dataframe
table = pd.DataFrame(data=data, columns=headers)
# Save data frame as an html file
table.to_html("frame.html")
# Create new CSV file with the same name in the original file's directory
newpath = "{}/{}.csv".format(os.path.dirname(args.path), os.path.basename(args.path).split('.')[0])
open(newpath, 'w')
# Write data from datasframe to CSV file
table.to_csv(newpath, index=False)
print("Successfully created {}.csv in {}".format( os.path.basename(args.path).split('.')[0], os.path.dirname(args.path)))
