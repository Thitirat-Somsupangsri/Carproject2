import csv
import os


def update_word_time_csv(word_length, time_taken, filename='word_time_data.csv'):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['word_length', 'total_time', 'count', 'average_time'])

    data = {}
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            length = int(row['word_length'])
            data[length] = {
                'total_time': float(row['total_time']),
                'count': int(row['count']),
                'average_time': float(row['average_time'])
            }

    if word_length in data:
        data[word_length]['total_time'] += time_taken
        data[word_length]['count'] += 1
        data[word_length]['average_time'] = data[word_length]['total_time'] / data[word_length]['count']
    else:
        data[word_length] = {
            'total_time': time_taken,
            'count': 1,
            'average_time': time_taken
        }

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['word_length', 'total_time', 'count', 'average_time'])
        for length, stats in data.items():
            writer.writerow([length, stats['total_time'], stats['count'], stats['average_time']])