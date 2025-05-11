import json
import csv

with open('player_data.json', 'r') as file:
    data = json.load(file)

csv_data = []
header = ['user', 'played count in mode1', 'best score in mode1', 'average time played in mode1',
          'played count in mode2', 'total wins in mode2', 'hints', 'highest streak']

for user, stats in data.items():
    row = [user] + [stats.get(key, '') for key in header[1:]]
    csv_data.append(row)


with open('player_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(csv_data)
