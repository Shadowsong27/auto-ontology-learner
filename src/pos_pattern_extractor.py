import logging

from src.common import *
from nltk.corpus import gutenberg

from src.handler import PosPatternHandler


class PosPatternExtractor:

    NGRAM_UPPER = 4

    def __init__(self):
        self.handler = PosPatternHandler()
        self.pattern_dict = {}

    def generate_pattern_stats(self):
        """
        The statistical distribution of POS tags are generated from NLTK
        Gutenberg Corpus and Web text, both accounted for the relatively
        formal English and Web like English.

        called for gutenberg: gutenberg.fileids()
        called for webtext: webtext.fileids()

        :return:
        """
        # update distribution dict
        self.update_dict_gutenberg()

        # for file_id in nltk.corpus.webtext.fileids():

        # insert distribution dict
        self.handler.truncate_pos_dist()

        # TODO: implement a better rule selection
        for pattern in self.pattern_dict.keys():
            if "NN" in pattern:
                if pattern[-2:] != "IN" and \
                                pattern[-2:] != "TO" and \
                                "CC" not in pattern and \
                                "CD" not in pattern and \
                                pattern[-2:] != "DT" and \
                                pattern[-2:] != "VBD" and \
                                pattern[:2] != "IN":
                    pair = (pattern, self.pattern_dict[pattern])
                    self.handler.insert_pos_pattern(pair)

        self.handler.commit()

    def update_dict_gutenberg(self):
        for file_id in nltk.corpus.gutenberg.fileids():
            logging.info("processing text: {}".format(file_id))

            text = gutenberg.raw(file_id)
            tagged_text = tag(text)

            for i in range(1, self.NGRAM_UPPER + 1):
                logging.info("currently at {} gram".format(i))
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

