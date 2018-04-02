"""

This class handles the statistical calculation of POS taggers
distribution in general English corpora.

The corpora used is Gutenberg, and the interface used is NLTK.

"""


import logging

from nltk.corpus import gutenberg
from common import *

from handler import PosPatternHandler


class PosPatternExtractor:

    NGRAM_UPPER = 4

    def __init__(self):
        self.handler = PosPatternHandler()
        self.pattern_dict = {}

    def generate_pattern_stats(self):
        logging.info("Truncate old distribution")
        self.handler.truncate_pos_dist()

        logging.info("Tag corpora with POS tagger")
        self._tag_corpora()

        logging.info("Generate new noun phrases distribution")
        self.generate_noun_phrase_stats()

        logging.info("Generate new verb phrases distribution")
        self.generate_verb_phrase_stats()

        logging.info("Process complete")

    def generate_noun_phrase_stats(self):
        for pattern in self.pattern_dict.keys():
            if "NN" in pattern:
                if pattern[-2:] != "IN" and \
                        pattern[-2:] != "TO" and \
                        "CC" not in pattern and \
                        "CD" not in pattern and \
                        pattern[-2:] != "DT" and \
                        pattern[-2:] != "VBD" and \
                        pattern[:2] != "IN":
                    pair = (pattern, self.pattern_dict[pattern], "noun")
                    self.handler.insert_pos_pattern(pair)

        self.handler.commit()

    def generate_verb_phrase_stats(self):
        for pattern in self.pattern_dict.keys():
            if "VB" in pattern:
                pair = (pattern, self.pattern_dict[pattern], "verb")
                self.handler.insert_pos_pattern(pair)

        self.handler.commit()

    def _tag_corpora(self):
        for file_id in nltk.corpus.gutenberg.fileids():
            logging.info("Process text: {}".format(file_id))

            text = gutenberg.raw(file_id)
            tagged_text = tag(text)

            for i in range(1, self.NGRAM_UPPER + 1):
                self._get_pos_pattern_distribution(tagged_text, i)

    def _get_pos_pattern_distribution(self, tagged_text, n):
        grams = find_ngrams(tagged_text, n)

        for item in grams:

            next_item = 0

            pattern = ""
            for i in range(n):
                current_tag = item[i][1]

                if current_tag.isalpha():
                    pattern += current_tag + " "
                else:
                    next_item = 1
                    break

            if next_item:
                continue

            pattern = pattern.strip()

            if pattern in self.pattern_dict:
                self.pattern_dict[pattern] += 1
            else:
                self.pattern_dict[pattern] = 1


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    PosPatternExtractor().generate_pattern_stats()

