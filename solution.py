import numpy as np
import pandas as pd
import re
import spacy
import nltk
from dictionary import Dictionary


class Solution:

    @staticmethod
    def text_processing(row):
        from nltk import word_tokenize

        text = row['text'].lower()
        tokens = word_tokenize(text)
        proc = []
        i = 0

        while i < len(tokens):
            if (i + 1 < len(tokens)) and \
                    (tokens[i] in ['добрый', 'доброе']) and (tokens[i + 1] in ['день', 'утро', 'вечер']):
                proc.append(tokens[i] + tokens[i + 1])
                i += 1
            else:
                proc.append(tokens[i])

            i += 1

        return ' '.join(proc)

    @staticmethod
    def check_greeting(row):
        from nltk import word_tokenize

        text = row['processed_text']
        tokens = word_tokenize(text)

        check = 0

        for token in tokens:
            if token in Dictionary.greetings:
                check = 1

        return 1 if check == 1 and row['role'] == 'manager' else 0

    @staticmethod
    def check_introduced_himself(row):
        from nltk import word_tokenize

        text = row['processed_text']
        tokens = word_tokenize(text)

        while len(tokens) < 3:
            tokens.append('')

        trigram = list(nltk.ngrams(tokens, 3))
        check = 0

        for x in trigram:
            for temp in Dictionary.introduced_himself:
                if re.match(temp, ' '.join(x)):
                    check = 1

        return 1 if check == 1 and row['role'] == 'manager' else 0

    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')

        self.data = pd.read_csv('test_data.csv')
        self.data['processed_text'] = self.data.apply(self.text_processing, axis=1)
        self.data['greeting'] = self.data.apply(self.check_greeting, axis=1)
        self.data['is_introduced_himself'] = self.data.apply(self.check_introduced_himself, axis=1)
        self.client = self.data.loc[self.data['role'] == 'client']
        self.manager = self.data.loc[self.data['role'] == 'manager']

    def get_greeting_phrases(self):
        return self.manager.loc[self.manager['greeting'] == 1][['dlg_id', 'line_n', 'role', 'text']]

    def get_introduced_himself(self):
        return self.manager.loc[self.manager['is_introduced_himself'] == 1][['dlg_id', 'line_n', 'role', 'text']]
