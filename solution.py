import numpy as np
import pandas
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

    @staticmethod
    def check_parting(row):
        from nltk import word_tokenize

        text = row['processed_text']
        tokens = word_tokenize(text)

        while len(tokens) < 2:
            tokens.append('')

        trigram = list(nltk.ngrams(tokens, 2))
        check = 0

        for x in trigram:
            for temp in Dictionary.parting:
                if ' '.join(x) == ' '.join(temp):
                    check = 1

        return 1 if check == 1 and row['role'] == 'manager' else 0

    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')

        self.data = pd.read_csv('test_data.csv')
        self.data['processed_text'] = self.data.apply(self.text_processing, axis=1)
        self.data['greeting'] = self.data.apply(self.check_greeting, axis=1)
        self.data['is_introduced_himself'] = self.data.apply(self.check_introduced_himself, axis=1)
        self.data['is_parting'] = self.data.apply(self.check_parting, axis=1)
        self.client = self.data.loc[self.data['role'] == 'client']
        self.manager = self.data.loc[self.data['role'] == 'manager']

    def get_greeting_phrases(self):
        return self.manager.loc[self.manager['greeting'] == 1][['dlg_id', 'line_n', 'role', 'text']]

    def get_introduced_himself(self):
        return self.manager.loc[self.manager['is_introduced_himself'] == 1][['dlg_id', 'line_n', 'role', 'text']]

    def get_names_managers(self):
        from nltk import word_tokenize

        data = self.manager.loc[self.manager['is_introduced_himself'] == 1]
        data_text = data['processed_text']
        names = set()

        for text in data_text:
            tokens = word_tokenize(text)

            while len(tokens) < 3:
                tokens.append('')

            trigram_list = list(nltk.ngrams(tokens, 3))

            for i in range(len(trigram_list)):
                trigram = trigram_list[i]

                if re.match(r'(\W|^)меня\sзовут(\W|$)', ' '.join(trigram)):
                    names.add(trigram[2])
                elif re.match(r'(\W|^)меня\s[а-я]{1,}\sзовут(\W|$)', ' '.join(trigram)):
                    names.add(trigram[1])
                elif re.match(r'(\W|^)(здравствуйте|да|добрыйдень|приветствую|доброеутро|добрыйвечер)\sс\sвами(\W|$)',
                              ' '.join(trigram)):
                    names.add(trigram_list[i + 1][0])
                elif re.match(r'(\W|^)(здравствуйте|да|добрыйдень|приветствую|доброеутро|добрыйвечер)\sэто(\W|$)',
                              ' '.join(trigram)):
                    names.add(trigram[2])

        return names

    def get_parting_phrases(self):
        return self.manager.loc[self.manager['is_parting'] == 1][['dlg_id', 'line_n', 'role', 'text']]

    def get_criterion_for_dialog(self):
        dlg_id_list = self.data['dlg_id'].unique()
        dlg_id_greeting_list = self.manager.loc[self.manager['greeting'] == 1]
        dlg_id_greeting_list = dlg_id_greeting_list['dlg_id'].unique()
        dlg_id_parting_list = self.manager.loc[self.manager['is_parting'] == 1]
        dlg_id_parting_list = dlg_id_parting_list['dlg_id'].unique()

        res = pd.DataFrame(columns=['dlg_id', 'is_correct'])

        for dlg_id in dlg_id_list:
            if dlg_id in dlg_id_greeting_list and dlg_id in dlg_id_parting_list:
                res.loc[len(res), res.columns] = dlg_id, True
            else:
                res.loc[len(res), res.columns] = dlg_id, False

        return res
