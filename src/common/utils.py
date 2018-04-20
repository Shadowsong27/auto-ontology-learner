from bs4 import BeautifulSoup

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


def build_clean_soup(body):
    soup = BeautifulSoup(body, 'lxml')
    # simple cleaning
    for script in soup("script"):
        script.decompose()
    return soup


class BaseParser:

    def __init__(self, candidate, context=None):
        self.candidate = candidate
        self.context = context

    def execute(self):
        if self._has_probability():
            return self._parse()
        else:
            return None

    def _parse(self):
        """
        The result of parsing should contain
        1. primary search
        2. secondary search
        3. tertiary search
        4. search type
        5. hashed parse
        :return:
        """
        raise NotImplementedError

    def _has_probability(self):
        raise NotImplementedError
