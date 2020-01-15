import re

import pandas as pd
from translate import Translator
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from rippletagger.tagger import Tagger
import nltk


# Returneaza numarul de cuvinte din text
def count_of_words(text):
    return len(text.split(' '))


# Traducere in engleza
def trans_to_eng(text):
    trans = Translator(from_lang="romanian", to_lang="english")

    translation = trans.translate(text)

    return translation



# Traducere in romana
def trans_to_ro(text):
    trans = Translator(from_lang="english", to_lang="romanian")

    translation = trans.translate(text)

    return translation


# Returneaza partea de vorbire a unui cuvant
def get_type(word):
    return Tagger(language='ro').tag(word)


# Elimina adjectivele si adverbele
def delete_adj_adv(text):
    tokenized = sent_tokenize(text)
    good_words = []
    old = len(text.split(' '))

    for index in tokenized:
        words_list = nltk.word_tokenize(index)

        tagged = Tagger(language='ro')  # Using a Tagger. Which is part-of-speech  tagger or POS-tagger.

        for words in words_list:
            typed = tagged.tag(words)
            if typed[0][1] != 'ADJ' and typed[0][1] != 'ADV':

                good_words.append(typed[0][0])
            else:
                last_word = good_words[len(good_words) - 1]
                if get_type(last_word)[0][1] == "ADP" or get_type(last_word)[0][1] == "DET":
                    good_words.append(typed[0][0])

    new_text = ""
    for words in good_words:
        if words in ".,?!":
            new_text = new_text + words
        else:
            new_text = new_text + " " + words

    return new_text, old - len(new_text.split(' '))


# Returneaza hypernimul unui cuvant (il folosim pentru enumerare)
def get_hyper(word):
    new_text = trans_to_eng(word)

    syns = wordnet.synsets(new_text)
    if len(syns) != 0:
        if len(syns[0].hypernyms()) != 0:
            hypern = syns[0].hypernyms()[0].lemmas()[0].name()
            return hypern
    return word

# Eliminam enumerarile
def remove_enum(text):
    pattern = "[A-Za-z]+,[' ']"
    match = re.findall(pattern, text)
    text_for_changing = ""
    ltype = []

    if match is not None:
        for index in match:
            text_for_changing = text_for_changing + index
            index = index.replace(',', '')
            value = get_hyper(index)
            if value is not None:
                ltype.append(value)

    ltype = list(dict.fromkeys(ltype))
    if len(ltype) == 1:
        text = text.replace(text_for_changing, str(ltype[0]) + ", ")

    return text


# ELIMINAREA CITATELOR
def remove_quotes(text):
    pattern = "\"(.*?)\""
    pattern2 = "\'\'(.*?)\'\'"
    match = re.findall(pattern, text)
    match2 = re.findall(pattern2, text)
    count = 0

    if match is not None:
        for index in match:
            text = text.replace('\"' + index + '\"', '')
            count = count + len(index.split(' '))

    if match2 is not None:
        for index in match2:
            text = text.replace('\'\'' + index + '\'\'', '')
            count = count + len(index.split(' '))

    return text, count


# ELIMINAREA PARANTEZELOR
def remove_brackets(text):
    pattern = "\((.*?)\)"
    match = re.findall(pattern, text)
    original_length = len(text.split(' '))
    count = 0

    if match is not None:
        for index in match:
            text = text.replace('(' + index + ')', '')
            count = count + len(index.split(' '))

    return text, count


# ELIMINAREA DIALOGULUI
def removeDialogue(text):
    formatted_output = text.replace('\n', '\\n')
    splitted = formatted_output.split('\\n')
    l = []
    count = 0

    for index in range(0, len(splitted) - 1):
        if splitted[index] != '':
            if splitted[index][0] != '-':
                l.append(splitted[index])
            else:
                count = count + len(splitted[index].split(' '))

    text = ' '.join(word for word in l)
    return text, count


def isCountry(country):
    country = trans_to_eng(country)
    country = country.upper()
    df = pd.read_csv("timesData.csv")

    input_country_list = list(df['country'])
    input_country_list = [element.upper() for element in input_country_list]
    input_country_list = list(dict.fromkeys(input_country_list))
    if country in input_country_list:
        return True

    return False


def words_score(text):
    original = text
    separatori = [",", '.', '!', '?']
    tokenized = sent_tokenize(text)
    top_sentences = {}
    dictionary = {}

    for i in tokenized:

        for index in separatori:
            i = i.replace(index, '')

        words_list = nltk.word_tokenize(i)

        tagged = Tagger(language='ro')
        for words in words_list:
            type = tagged.tag(words)

            if type[0][0] not in dictionary.keys():
                if type[0][1] == 'PROPN':
                    dictionary[type[0][0]] = 2
                elif type[0][1] == 'VERB':
                    dictionary[type[0][0]] = 1
                elif type[0][1] == 'NOUN':
                    dictionary[type[0][0]] = 0.5
                else:
                    dictionary[type[0][0]] = 0.1
            else:
                if type[0][1] == 'PROPN':
                    dictionary[type[0][0]] += 2
                elif type[0][1] == 'VERB':
                    dictionary[type[0][0]] += 1
                elif type[0][1] == 'NOUN':
                    dictionary[type[0][0]] += 0.5
                else:
                    dictionary[type[0][0]] += 0.1

    for i in tokenized:
        copy = i
        for index in separatori:
            i = i.replace(index, '')

        words_list = nltk.word_tokenize(i)
        suma = 0
        for words in words_list:
            if words in dictionary.keys():
                suma = suma + dictionary[words]
        top_sentences[copy] = suma

    return top_sentences


def summary_status(total, current_length, percentage):
    if current_length > total - int(((percentage * total) / 100)):
        return True
    return False


def words_in_mylist(mylist):
    count = 0
    for index in mylist:
        count = count + count_of_words(index[0])
    return count
