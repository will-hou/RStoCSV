# Removes a scout if the "Name" metric is empty
def remove_repeats(json_data):
    repeats = []
    for (team_key, team) in json_data['teams'].items():
        for scout in team:
            for (metric_key, metric) in scout['metrics'].items():
                if metric['name'] == "Name" and metric['value'] is None:
                    repeats.append([team_key, team.index(scout), metric_key])
    for i in repeats:
        del (json_data['teams'][i[0]][i[1]])
    print("Deleted {} empty scouts".format(len(repeats)))
