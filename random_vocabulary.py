import random
import csv


class Vocabulary:
    def __init__(self, csv_file):
        self.__words = self.load_words(csv_file)

    @staticmethod
    def load_words(csv_file):
        words = {}
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if len(row) == 3:
                    word, part_of_speech, definition = row
                    words[word.lower()] = {
                        'part_of_speech': part_of_speech,
                        'definition': definition
                    }
        return words

    def random_word(self):
        word = random.choice(list(self.__words.keys()))
        return {
            'word': word,
            'part_of_speech': self.__words[word]['part_of_speech'],
            'definition': self.__words[word]['definition']
        }
