import logging

from nltk.corpus import gutenberg
from src.common.constants import NGRAM_UPPER_THRESHOLD, NOUN_PHRASE_THRESHOLD, VERB_PHRASE_THRESHOLD
from src.common.model import Keyword
from src.common.handler import PosPatternHandler
from src.common.utils import *


class PosPatternExtractor:
    """
    This class handles the statistical calculation of POS taggers
    distribution in general English corpora.

    The corpora used is Gutenberg, and the interface used is NLTK.

    """

    def __init__(self, corpora=None):
        self.corpora = corpora
        self.handler = PosPatternHandler()
        self.pattern_dict = {}

    def generate_pattern_stats(self, ):
        logging.info("Truncate old distribution")
        self.handler.truncate_pos_dist()

        logging.info("Tag corpora with POS tagger")
        self._tag_corpora()

        logging.info("Generate new noun phrases distribution")
        self._generate_noun_phrase_stats()

        logging.info("Generate new verb phrases distribution")
        self._generate_verb_phrase_stats()

        logging.info("Process complete")

    def _generate_noun_phrase_stats(self):
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

    def _generate_verb_phrase_stats(self):
        for pattern in self.pattern_dict.keys():

            if "VB" in pattern:
                pair = (pattern, self.pattern_dict[pattern], "verb")
                self.handler.insert_pos_pattern(pair)

        self.handler.commit()

    def _tag_corpora(self):
        """
        will generate the POS distribution from Gutenberg corpora
        by default
        allows customised corpora as well
        :param corpora: list of str -> a list of corpus
        :return: None
        """
        if self.corpora is None:
            for file_id in nltk.corpus.gutenberg.fileids():
                text = gutenberg.raw(file_id)
                self._get_pos_distribution(text)
        else:
            for text in self.corpora:
                self._get_pos_distribution(text)

    def _get_pos_distribution(self, text):
        tagged_text = tag(text)
        for i in range(1, NGRAM_UPPER_THRESHOLD + 1):
            grams = find_ngrams(tagged_text, i)
            for item in grams:
                next_item = 0
                pattern = ""
                for cur_gram in range(i):
                    current_tag = item[cur_gram][1]

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


class SimpleKeywordsExtractor:

    def __init__(self, phrase_type):
        self.handler = PosPatternHandler()

        if phrase_type == 'noun':
            self.candidate_pattern = list(map(lambda x: x[0],
                                              self.handler.get_patterns_above_ratio_for_noun(NOUN_PHRASE_THRESHOLD)))
        else:
            self.candidate_pattern = list(map(lambda x: x[0],
                                              self.handler.get_patterns_above_ratio_for_verb(VERB_PHRASE_THRESHOLD)))

    def generate_keywords(self, target_text):
        """main logic to generate final keywords list"""
        logging.debug("Start generate keywords")
        sentences = text_to_sentences(target_text)

        base_candidates = self._generate_base_candidates(target_text)

        temp_result = []
        for item in zip(base_candidates, base_candidates[1:]):
            temp_result += self._upward_grouping(*item)

        # convert str into objects
        temp_result = [Keyword(text=item) for item in temp_result]
        temp_result = self._mark_keyword_attributes(sentences, temp_result)

        # check overlapping, could be combined into one word
        return self._merge_keywords(sentences, temp_result)

    def _generate_base_candidates(self, target_text):
        """generate base candidates based on ratio threshold"""

        result_list = []
        tagged_text = tag(target_text)

        for i in range(1, 5):
            temp = []
            grams = find_ngrams(tagged_text, i)

            for gram in grams:
                phrase = " ".join(list(map(lambda x: x[0], gram)))
                pos = " ".join(list(map(lambda x: x[1], gram)))

                if pos in self.candidate_pattern:
                    temp.append(phrase)

            result_list.append(temp)

        return result_list

    @staticmethod
    def _upward_grouping(pre_list, tar_list):
        """
        given two list of candidates
        pre_list: one gram lesser than tar_list
        group potential candidates together by substring grouping
        """
        result = set()
        for pre in pre_list:
            for tar in tar_list:
                if pre in tar:
                    result.add(pre)

        return list(set(pre_list) - result)

    @staticmethod
    def _merge_keywords(sentences, temp_result):
        final = {}
        for i in range(len(sentences)):
            logging.debug("sentence {}".format(i))
            keywords_group = list(filter(lambda x: x.sentence_index == i, temp_result))
            keywords_group.sort(key=lambda x: x.sentence_start_pos)
            for item in zip(keywords_group, keywords_group[1:]):
                keyword_1, keyword_2 = item
                if keyword_1.sentence_end_pos >= keyword_2.sentence_start_pos:
                    new_text = sentences[i][keyword_1.sentence_start_pos: keyword_2.sentence_end_pos].strip()
                    new_keyword = Keyword(new_text)
                    new_keyword.sentence_start_pos = keyword_1.sentence_start_pos
                    new_keyword.sentence_end_pos = keyword_2.sentence_end_pos
                    new_keyword.sentence_index = i
                    final[new_text] = new_keyword
                else:
                    final[keyword_1.text] = keyword_1
                    final[keyword_2.text] = keyword_2

        return [value for value in final.values()]

    @staticmethod
    def _mark_keyword_attributes(sentences, temp_result):
        for i in range(len(sentences)):
            sentence = sentences[i]
            for keyword in temp_result:
                if keyword.text in sentence:
                    keyword.sentence_start_pos = sentence.index(keyword.tokens[0])
                    keyword.sentence_end_pos = keyword.sentence_start_pos + len(keyword.text)
                    keyword.sentence_index = i

        return temp_result


class SimpleRelationsExtractor:

    def __init__(self):
        self.handler = PosPatternHandler()
        self.ke_n = SimpleKeywordsExtractor('noun')
        self.ke_v = SimpleKeywordsExtractor('verb')

    def generate_relations(self, target_text):
        relations = []
        noun_phrases = self.ke_n.generate_keywords(target_text)
        verb_phrases = self.ke_v.generate_keywords(target_text)
        sentences = text_to_sentences(target_text)

        for i in range(len(sentences)):
            sentence = sentences[i]
            cur_nouns = list(filter(lambda x: x.sentence_index == i, noun_phrases))
            cur_verbs = list(filter(lambda x: x.sentence_index == i, verb_phrases))

            logging.debug(cur_nouns)

            if len(cur_nouns) == 2:
                for item in cur_verbs:
                    relations.append((
                        cur_nouns[0],
                        cur_nouns[1],
                        item,
                        sentence
                    ))
            elif len(cur_nouns) == 1:
                for item in cur_verbs:
                    relations.append((
                        cur_nouns[0],
                        None,
                        item,
                        sentence
                    ))
            else:
                for noun_item in zip(cur_nouns, cur_nouns[1:]):
                    lower = noun_item[0].sentence_start_pos
                    upper = noun_item[1].sentence_end_pos

                    for item in verb_phrases:
                        if lower < item.sentence_start_pos < upper:
                            relations.append((
                                noun_item[0],
                                noun_item[1],
                                item,
                                sentence
                            ))

        return relations


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    PosPatternExtractor().generate_pattern_stats()


