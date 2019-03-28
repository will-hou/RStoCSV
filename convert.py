import argparse
import json
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import numpy as np
import pandas as pd

from utils import *

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filter', help="whether or not to remove empty scouts", default=False)
parser.add_argument('-t', '--timestamp',
                    help="Whether or not to include scout timestamps in the CSV file. ONLY USE with data from Robot Scouter version 3.0.0-beta2 and above ",
                    action="store_true")
parser.add_argument('-e', '--save_filtered', help="Whether to just format the JSON file and not perform conversions",
                    action="store_true")
args = parser.parse_args()

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
file_path = askopenfilename(
    filetypes=[("JSON files", '*.json')])  # show an "Open" dialog box and return the path to the selected file
print("Converting {} into a CSV file".format(file_path))
print("Filtering: {}, With Timestamps: {}".format(args.filter, args.timestamp))

try:
    with open(file_path) as file:
        json_data = json.load(file)
except json.decoder.JSONDecodeError:
    print("Invalid JSON file! Make sure your file is a true JSON file")
    exit()

if args.timestamp:
    try:
        json_data['teams'][list(json_data['teams'].keys())[0]][0]['timestamp']
    except KeyError:
        print(
            "The JSON file you uploaded does not have a timestamp value. Try running the program without the -t flag. Use --help for more info")
        exit()

# Filter the data, if needed
filter(json_data, args.filter) if args.filter else None

# Export filtered data and stop conversion, if specified
if args.save_filtered:
    newpath = "{}/{}_filtered.json".format(os.path.dirname(file_path), os.path.basename(file_path).split('.')[0])
    with open(newpath, 'w') as fp:
        json.dump(json_data, fp)
    print("Successfully created {}.json in {}".format(os.path.basename(file_path).split('.')[0],
                                                      os.path.dirname(file_path)))
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

# Preallocate numpy array with number of scouts and the number of metrics.
# Add two columns for team numbers and scout names. Add an extra column for timestamps, if needed.
num_metrics = num_metrics + 2 + (1 if args.timestamp else 0)
data = np.zeros((num_scouts, num_metrics), dtype='O')

# List of all metrics scouted
headers = [i['name'] for i in json_data['teams'][list(json_data['teams'].keys())[0]][0]['metrics'].values()]
# Add team number and name of scout to the CSV . Add timestamp header, if needed
headers.insert(0, "Timestamp") if args.timestamp else None
headers.insert(0, "Name of Scout")
headers.insert(0, "Team Number")

# Put scout data into a numpy array
row = 0
# Find which column we should add the metrics to
column = 3 if args.timestamp else 2
for team in json_data['teams'].values():
    for scout in team:
        # Add the name of the scout to the data matrix
        data[row, 1] = scout['name']
        # Add the timestamp of the scout to the data matrix, if needed
        data[row, 2] = scout['timestamp'] if args.timestamp else None
        # Adds all the metric values to a list. If the metric value is a string, remove duplicated spaces and tabs
        metric_values = [" ".join(i['value'].split()) if type(i['value']) is str else i['value'] for i in
                         scout['metrics'].values()]
        # Check to make sure that the metric values exist before adding to the data matrix
        data[row, column:] = metric_values if (len(metric_values) + column) == len(headers) else None
        row += 1

# Put team numbers into data matrix
team_nums = []
for team in json_data["teams"]:
    for i in range(0, len(json_data["teams"][team])):
        team_nums.append(team)
data[:, 0] = team_nums

# Convert array into dataframe
table = pd.DataFrame(data=data, columns=headers)
# Save data frame as an html file
table.to_html("frame.html")
# Create new CSV file with the same name in the original file's directory
newpath = "{}/{}.csv".format(os.path.dirname(file_path), os.path.basename(file_path).split('.')[0])
try:
    open(newpath, 'w')
except PermissionError:
    print("The file you're trying to convert can't be inside the RStoCSV directory!")
    exit()
# Write data from dataframe to CSV file
table.to_csv(newpath, index=False)
print("Successfully created {}.csv in {}".format(os.path.basename(file_path).split('.')[0], os.path.dirname(file_path)))
