import argparse
import json
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("path", help="the path to the JSON file you want to convert", type=str)
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

team_nums = []

# TODO: Add team number and match number to array
for team in json_data["teams"]:
    for i in range(0, len(json_data["teams"][team])):
        team_nums.append(team)

team_nums = np.vstack(np.asarray(team_nums))

data = np.concatenate((team_nums, data), axis=1)

print(team_nums.shape, data.shape)
print(data.shape)

headers.insert(0, "Team Number")




# Convert array into dataframe
table = pd.DataFrame(data=data, columns=headers)
# Save data frame as an html file
table.to_html("frame.html")

# Convert data frame to csv
table.to_csv("scout.csv", index=False)
