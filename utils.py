# Removes a scout if user specified metric is empty
def filter(json_data, metric_to_filter):
    repeats = []
    num_empty = strip_empty_metrics(json_data)
    for (team_key, team) in json_data['teams'].items():
        for scout in team:
            for (metric_key, metric) in scout['metrics'].items():
                if metric['name'].strip() == metric_to_filter and metric['value'] is None:
                    repeats.append([team_key, team.index(scout), metric_key])

    # Compensates for index modification after deletion from list
    # Keeps track of how many index values to subtract if a team shows up more than once on the repeats list
    tracker = {}
    for i in repeats:
        index = i[1] - tracker.get(i[0]) if tracker.get(i[0]) is not None else i[1]
        del json_data['teams'][i[0]][index]
        if i[0] not in tracker:
            tracker[i[0]] = 1
        else:
            tracker[i[0]] += 1
    print("Deleted {} empty scouts".format(len(repeats) + num_empty))
    return json_data


# TODO: Find way to incorporate this in the filter function
def strip_empty_metrics(json_data):
    to_delete = []
    for (team_key, team) in json_data['teams'].items():
        for scout in team:
            if len(scout['metrics'].items()) == 0:
                to_delete.append([team_key, team.index(scout)])
    for i in to_delete:
        del json_data['teams'][i[0]][i[1]]
    return len(to_delete)
