import string
import nltk
import re


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


def remove_punctuation(sentence):
    translator = str.maketrans('', '', string.punctuation)
    return sentence.translate(translator)


def text_to_sentences(text):
    return re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)


def tag(text):
    text = nltk.word_tokenize(text)
    return nltk.pos_tag(text)
