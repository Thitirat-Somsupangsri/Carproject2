import csv


input_file = 'wordDictionary.txt'
output_file = 'filtered_dictionary.csv'
non_repititive = set()

with open(input_file, 'r', encoding='utf-8') as infile, \
        open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['word', 'part of speech', 'definition'])

    for line in infile:
        parts = line.strip().split('|')


        if len(parts) >= 3:
            word = parts[0].strip()
            part_of_speech = parts[1].strip()
            definition = parts[2].strip()


            if len(word) > 1 and part_of_speech and definition and word not in non_repititive :
                writer.writerow([word, part_of_speech, definition])

print("completed")
