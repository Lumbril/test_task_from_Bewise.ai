import numpy as np
import pandas as pd
import re
import nltk
import spacy

nltk.download('punkt')
nltk.download('stopwords')


class Dictionary:
    greetings = ['здравствуйте', 'приветствую', 'добрыйдень', 'доброеутро', 'добрыйвечер']


class Solution:

    @staticmethod
    def text_processing(row):
        from nltk import word_tokenize
        from nltk.corpus import stopwords

        text = row['text']
        tokens = word_tokenize(text)

        stop_words = list(stopwords.words('russian'))

        tokens = [word for word in tokens if word not in stop_words]
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

    def __init__(self):
        self.data = pd.read_csv('test_data.csv')
        self.data['text'] = self.data['text'].apply(lambda x: x.lower())
        self.data['processed_text'] = self.data.apply(self.text_processing, axis=1)
        self.data['greeting'] = self.data.apply(self.check_greeting, axis=1)
        self.client = self.data.loc[self.data['role'] == 'client']
        self.manager = self.data.loc[self.data['role'] == 'manager']

    def get_greeting_phrases(self):
        return self.manager.loc[self.manager['greeting'] == 1][['dlg_id', 'line_n', 'role', 'text']]


solution = Solution()

menu = 'Номера действий:\n' \
       '1 - Извлечь реплики с приветствием – где менеджер поздоровался\n' \
       '0 - Завершить работу\n' \
       'Введите номер действия: '
x = input(menu)

while True:
    if not x.isnumeric():
        raise Exception('Введенное значение не число, досрочное завершение программы')

    x = int(x)

    if x == 0:
        break
    elif x == 1:
        data = solution.get_greeting_phrases()
        print(data.head(15))

    x = input(menu)
